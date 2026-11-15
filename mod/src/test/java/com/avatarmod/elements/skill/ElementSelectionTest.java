package com.avatarmod.elements.skill;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class ElementSelectionTest {

    @Test
    void cyclesThroughElementsInSelectorOrderAndWraps() {
        String element = "FIRE";

        element = ElementSlotMap.nextElement(element);
        assertEquals("AIR", element);
        element = ElementSlotMap.nextElement(element);
        assertEquals("WATER", element);
        element = ElementSlotMap.nextElement(element);
        assertEquals("EARTH", element);
        element = ElementSlotMap.nextElement(element);
        assertEquals("FIRE", element);
    }

    @Test
    void invalidElementRecoversToFirstConfiguredElement() {
        assertEquals("FIRE", ElementSlotMap.nextElement("UNKNOWN"));
    }
}
