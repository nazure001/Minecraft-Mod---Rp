# Debug Report — Element Switching Bug (2026-11-14)

## 🔍 **Suspect Code Location**

### File 1: `AvatarElementsClient.java` (Client element wheel handler)

**Location:** Lines 78–94

```java
if (elementCycleCooldown > 0) {
    elementCycleCooldown--;
}

int wheelCode = getKeyCode(AvatarKeyBindings.ELEMENT_WHEEL);
boolean wheelDown = (client.currentScreen == null) && (wheelCode > 0)
        && net.minecraft.client.util.InputUtil.isKeyPressed(client.getWindow().getHandle(), wheelCode);

if (wheelDown && !wheelWasDown && elementCycleCooldown == 0) {
    elementCycleCooldown = 6; // 300ms debounce
    ClientPlayNetworking.send(new SkillPackets.C2SCycleElement());
}
wheelWasDown = wheelDown;
```

**Assessment:** Client-side logic looks correct:
- Cooldown properly decremented ✅
- Debounce check `!wheelWasDown` prevents spam ✅
- BUT: Potential issue if `ELEMENT_WHEEL` key binding conflicts with another key

### File 2: `SkillNetworking.java` (Server element cycle handler)

**Location:** Lines 302–319

```java
public static void registerCycleElementReceiver() {
    ServerPlayNetworking.registerGlobalReceiver(
            SkillPackets.C2SCycleElement.ID,
            (payload, context) -> {
                ServerPlayerEntity player = context.player();
                PlayerBendingData data = PlayerBendingData.get(player);
                if (!data.getTimeline().isIdle()) {
                    data.getTimeline().cancel();
                    broadcastOrbReset(player);
                }
                String element = ElementSlotMap.nextElement(data.getActiveElement());
                data.setActiveElement(element);
                ServerPlayNetworking.send(player, new SkillPackets.S2CSyncElement(element));
                player.sendMessage(
                        Text.literal("[Avatar] Element: " + element), true);
            });
}
```

**Assessment:** Server logic correct, BUT:
- ❌ NO VALIDATION that player actually sent the cycle request (could be spoofed)
- ❌ NO DEBOUNCE on server side (relies entirely on client 300ms throttle)

### File 3: `PlayerBendingData.java` (Element state storage)

**Location:** Lines 44–45, 177–179

```java
private String activeElement = "FIRE";  // Default

public static PlayerBendingData get(ServerPlayerEntity player) {
    return player.getAttachedOrCreate(ATTACHMENT);
}
```

**Assessment:** Potential issue:
- ⚠️ `getAttachedOrCreate` will RESET activeElement to "FIRE" if attachment lost
- ⚠️ No persistence check — if attachment is evicted from memory, state lost
- ⚠️ Could cause element to "randomly" reset if attachment GC'd or server reload

---

## 🎯 **Three Possible Root Causes**

### Cause 1: Keybind Conflict 🟠

**Hypothesis:** `AvatarKeyBindings.ELEMENT_WHEEL` key code overlaps with another keybind (maybe modifier key or special key).

**Test:** Check if ELEMENT_WHEEL is set and what its default/current keybind is.

**Check code:**
```bash
grep -r "ELEMENT_WHEEL" mod/src/main/java/com/avatarmod/elements/ --include="*.java"
```

### Cause 2: Concurrent PlayerBendingData Creation 🟠

**Hypothesis:** Race condition in `getAttachedOrCreate()` — two threads call it simultaneously, both create new instances, state resets.

**Symptom:** Element randomly resets to FIRE or changes without user input.

**Fix:** Synchronize or add double-check lock in `PlayerBendingData.get()`.

### Cause 3: Element Sync Desync Between Client & Server 🟠

**Hypothesis:** Client HUD shows old element, server has new one. When skill cast, server uses its element (wrong one) while client expects old one.

**Symptom:** Player cycles element → client shows it → cast skill using OLD element from server.

**Fix:** Ensure `S2CSyncElement` packet always sent on element change + client stores it properly.

---

## 🔧 **Diagnosis Steps**

### Step 1: Confirm keybind is not NULL or conflicting

```bash
grep -A2 -B2 "ELEMENT_WHEEL" mod/src/main/java/com/avatarmod/elements/client/AvatarKeyBindings.java
```

If keybind is not set or conflicts with Z/X/C/V/B, **FIX #1**.

### Step 2: Check PlayerBendingData attachment lifecycle

Test: Add server log when PlayerBendingData is created:
```java
public PlayerBendingData() {
    AvatarElementsMod.LOGGER.info("[Avatar] New PlayerBendingData created, activeElement = {}", activeElement);
    // ...
}
```

If log shows creation multiple times per session = **Cause 2: Race condition**.

### Step 3: Add element sync verification

Test: After server sends `S2CSyncElement`, log it:
```java
String element = ElementSlotMap.nextElement(data.getActiveElement());
data.setActiveElement(element);
AvatarElementsMod.LOGGER.info("[Avatar] Element changed to {} for player {}", element, player.getName().getString());
ServerPlayNetworking.send(player, new SkillPackets.S2CSyncElement(element));
```

Compare with client-side `ElementWheelRenderer.setElement()` log.

---

## 🛠️ **Proposed Fixes**

### Fix 1: Add Server-Side Debounce

```java
// Server: Add per-player cooldown for element cycling
private static final Map<UUID, Integer> elementCycleCooldown = new HashMap<>();

public static void registerCycleElementReceiver() {
    ServerPlayNetworking.registerGlobalReceiver(
            SkillPackets.C2SCycleElement.ID,
            (payload, context) -> {
                ServerPlayerEntity player = context.player();
                UUID uuid = player.getUuid();
                
                // Check server-side cooldown
                int cooldown = elementCycleCooldown.getOrDefault(uuid, 0);
                if (cooldown > 0) {
                    elementCycleCooldown.put(uuid, cooldown - 1);
                    return; // Ignore packet
                }
                
                PlayerBendingData data = PlayerBendingData.get(player);
                if (!data.getTimeline().isIdle()) {
                    data.getTimeline().cancel();
                    broadcastOrbReset(player);
                }
                String element = ElementSlotMap.nextElement(data.getActiveElement());
                data.setActiveElement(element);
                elementCycleCooldown.put(uuid, 6); // 300ms debounce
                
                ServerPlayNetworking.send(player, new SkillPackets.S2CSyncElement(element));
            });
}

// Also reset on player disconnect
public static void onPlayerDisconnect(UUID uuid) {
    elementCycleCooldown.remove(uuid);
    // ...existing cleanup
}
```

### Fix 2: Synchronize PlayerBendingData Access

```java
public static synchronized PlayerBendingData get(ServerPlayerEntity player) {
    return player.getAttachedOrCreate(ATTACHMENT);
}
```

Or safer: Double-check lock pattern in Attachment.

### Fix 3: Validate Element Before Setting

```java
public void setActiveElement(String element) {
    String[] validElements = ElementSlotMap.ELEMENTS;
    boolean valid = false;
    for (String valid_elem : validElements) {
        if (valid_elem.equals(element)) {
            valid = true;
            break;
        }
    }
    if (valid) {
        this.activeElement = element;
    } else {
        AvatarElementsMod.LOGGER.warn("[Avatar] Invalid element: {}, keeping {}", element, activeElement);
    }
}
```

---

## 📋 **Action Plan**

1. **Check keybind** — Run grep to see ELEMENT_WHEEL definition
   - If NULL or conflict → FIX #1 (add server debounce)
   - If OK → Check Cause 2

2. **Add logging** — Insert logs in PlayerBendingData constructor + server element change
   - If multiple creations → FIX #2 (synchronize)
   - If sync mismatch → FIX #3 (validate)

3. **Test** — Re-test element cycling in-game after fix

4. **Commit** — Document the fix in commit message

---

## 🔴 **Priority: IMMEDIATE**

This bug blocks all Wave 2 testing. Estimate: 30 minutes to debug + 15 minutes to fix.

