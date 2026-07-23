package com.example

import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onRoot
import com.example.ui.theme.MyApplicationTheme
import com.github.takahirom.roborazzi.captureRoboImage
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode

@RunWith(RobolectricTestRunner::class)
@GraphicsMode(GraphicsMode.Mode.NATIVE)
class CalculatorScreenshotTest {

    @get:Rule val composeTestRule = createComposeRule()

    @Test
    @Config(qualifiers = "w800dp-h1280dp", sdk = [34])
    fun tablet_portrait() {
        composeTestRule.setContent { MyApplicationTheme { CalculatorApp() } }
        composeTestRule.onRoot().captureRoboImage(filePath = "src/test/screenshots/tablet_portrait.png")
    }

    @Test
    @Config(qualifiers = "w1280dp-h800dp", sdk = [34])
    fun tablet_landscape() {
        composeTestRule.setContent { MyApplicationTheme { CalculatorApp() } }
        composeTestRule.onRoot().captureRoboImage(filePath = "src/test/screenshots/tablet_landscape.png")
    }
}
