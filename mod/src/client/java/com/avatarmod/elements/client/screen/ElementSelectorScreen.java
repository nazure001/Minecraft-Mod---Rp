package com.avatarmod.elements.client.screen;

import com.avatarmod.elements.client.hud.ElementWheelRenderer;
import com.avatarmod.elements.client.network.SkillClientHandler;
import com.avatarmod.elements.skill.ElementSlotMap;
import net.minecraft.client.gui.DrawContext;
import net.minecraft.client.gui.screen.Screen;
import net.minecraft.text.Text;
import org.lwjgl.glfw.GLFW;

public final class ElementSelectorScreen extends Screen {

    private static final String[] ELEMENTS = ElementSlotMap.ELEMENTS.clone();
    private static final int OPTION_WIDTH = 76;
    private static final int OPTION_HEIGHT = 24;
    private static final int[] POSITION_BY_ELEMENT = {1, 0, 2, 3, 4};

    private int selectedIndex;
    private boolean keyboardNavigation;

    public ElementSelectorScreen() {
        super(Text.translatable("gui.avatar_elements.element_selector.title"));
        selectedIndex = findElementIndex(ElementWheelRenderer.getCurrentElement());
    }

    @Override
    public void render(DrawContext context, int mouseX, int mouseY, float delta) {
        context.fill(0, 0, width, height, 0xA8000000);

        int centerX = width / 2;
        int centerY = height / 2 + 8;
        int radius = radialRadius();

        context.drawCenteredTextWithShadow(
                textRenderer, title, centerX, Math.max(12, centerY - radius - 40), 0xFFFFFFFF);
        context.drawCenteredTextWithShadow(
                textRenderer,
                Text.translatable("gui.avatar_elements.element_selector.active",
                        Text.translatable(elementTranslationKey(ElementWheelRenderer.getCurrentElement()))),
                centerX, Math.max(12, centerY - radius - 22), 0xFFE8D8C3);

        for (int i = 0; i < ELEMENTS.length; i++) {
            int position = POSITION_BY_ELEMENT[i];
            int x = optionX(position, centerX, radius);
            int y = optionY(position, centerY, radius);
            boolean hovered = !keyboardNavigation && mouseX >= x && mouseX < x + OPTION_WIDTH
                    && mouseY >= y && mouseY < y + OPTION_HEIGHT;
            boolean highlighted = hovered || i == selectedIndex;
            int color = ElementWheelRenderer.getElementColor(ELEMENTS[i]);

            context.fill(x - 2, y - 2, x + OPTION_WIDTH + 2, y + OPTION_HEIGHT + 2,
                    highlighted ? 0xFFE8D8C3 : 0xFF38291E);
            context.fill(x, y, x + OPTION_WIDTH, y + OPTION_HEIGHT,
                    highlighted ? color : (color & 0x00FFFFFF) | 0xD0000000);
            context.drawCenteredTextWithShadow(
                    textRenderer,
                    Text.translatable(elementTranslationKey(ELEMENTS[i])),
                    x + OPTION_WIDTH / 2, y + 8, 0xFFFFFFFF);
        }

        context.drawCenteredTextWithShadow(
                textRenderer,
                Text.translatable("gui.avatar_elements.element_selector.hint"),
                centerX, Math.min(height - 16, centerY + radius + 42), 0xFFE8D8C3);
    }

    @Override
    public void mouseMoved(double mouseX, double mouseY) {
        keyboardNavigation = false;
        int centerX = width / 2;
        int centerY = height / 2 + 8;
        int radius = radialRadius();
        for (int i = 0; i < ELEMENTS.length; i++) {
            int position = POSITION_BY_ELEMENT[i];
            int x = optionX(position, centerX, radius);
            int y = optionY(position, centerY, radius);
            if (mouseX >= x && mouseX < x + OPTION_WIDTH
                    && mouseY >= y && mouseY < y + OPTION_HEIGHT) {
                selectedIndex = i;
                break;
            }
        }
        super.mouseMoved(mouseX, mouseY);
    }

    @Override
    public boolean mouseClicked(double mouseX, double mouseY, int button) {
        if (button != 0) return super.mouseClicked(mouseX, mouseY, button);

        int centerX = width / 2;
        int centerY = height / 2 + 8;
        int radius = radialRadius();
        for (int i = 0; i < ELEMENTS.length; i++) {
            int position = POSITION_BY_ELEMENT[i];
            int x = optionX(position, centerX, radius);
            int y = optionY(position, centerY, radius);
            if (mouseX >= x && mouseX < x + OPTION_WIDTH
                    && mouseY >= y && mouseY < y + OPTION_HEIGHT) {
                selectedIndex = i;
                selectElement();
                return true;
            }
        }
        return true;
    }

    @Override
    public boolean keyPressed(int keyCode, int scanCode, int modifiers) {
        switch (keyCode) {
            case GLFW.GLFW_KEY_LEFT -> selectWithKeyboard(2);
            case GLFW.GLFW_KEY_UP -> selectWithKeyboard(1);
            case GLFW.GLFW_KEY_RIGHT -> selectWithKeyboard(0);
            case GLFW.GLFW_KEY_DOWN -> selectWithKeyboard(3);
            case GLFW.GLFW_KEY_ENTER, GLFW.GLFW_KEY_KP_ENTER, GLFW.GLFW_KEY_SPACE -> selectElement();
            default -> {
                return super.keyPressed(keyCode, scanCode, modifiers);
            }
        }
        return true;
    }

    @Override
    public boolean shouldPause() {
        return false;
    }

    private int radialRadius() {
        int horizontalLimit = width / 2 - OPTION_WIDTH / 2 - 4;
        int verticalLimit = height / 2 - OPTION_HEIGHT / 2 - 20;
        return Math.max(30, Math.min(64, Math.min(horizontalLimit, verticalLimit)));
    }

    private void selectElement() {
        SkillClientHandler.selectElement(ELEMENTS[selectedIndex]);
        close();
    }

    private void selectWithKeyboard(int elementIndex) {
        keyboardNavigation = true;
        selectedIndex = elementIndex;
    }

    private int optionX(int position, int centerX, int radius) {
        return switch (position) {
            case 1 -> centerX + radius - OPTION_WIDTH / 2;
            case 2 -> centerX - radius - OPTION_WIDTH / 2;
            default -> centerX - OPTION_WIDTH / 2;
        };
    }

    private int optionY(int position, int centerY, int radius) {
        return switch (position) {
            case 0 -> centerY - radius - OPTION_HEIGHT / 2;
            case 3 -> centerY + radius - OPTION_HEIGHT / 2;
            default -> centerY - OPTION_HEIGHT / 2;
        };
    }

    private static int findElementIndex(String element) {
        for (int i = 0; i < ELEMENTS.length; i++) {
            if (ELEMENTS[i].equals(element)) return i;
        }
        return 0;
    }

    private static String elementTranslationKey(String element) {
        return "element.avatar_elements." + element.toLowerCase(java.util.Locale.ROOT);
    }
}
