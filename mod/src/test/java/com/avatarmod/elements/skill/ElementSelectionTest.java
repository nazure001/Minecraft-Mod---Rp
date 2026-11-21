package com.avatarmod.elements.skill;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

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
        assertEquals("NON_BENDER", element);
        element = ElementSlotMap.nextElement(element);
        assertEquals("FIRE", element);
    }

    @Test
    void invalidElementRecoversToFirstConfiguredElement() {
        assertEquals("FIRE", ElementSlotMap.nextElement("UNKNOWN"));
    }

    @Test
    void acceptsOnlyConfiguredElementNames() {
        for (String element : ElementSlotMap.ELEMENTS) {
            assertTrue(ElementSlotMap.isElement(element));
        }
        assertFalse(ElementSlotMap.isElement("LIGHTNING"));
        assertFalse(ElementSlotMap.isElement("fire"));
        assertFalse(ElementSlotMap.isElement(null));
    }
}
