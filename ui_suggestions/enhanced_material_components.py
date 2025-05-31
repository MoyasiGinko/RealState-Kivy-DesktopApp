#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Material Design Components - UI Suggestions
Additional modern components to enhance your existing system
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Line, SmoothLine
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
import math


class RippleButton(ButtonBehavior, BoxLayout):
    """Material Design button with ripple effect"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ripple_color = [0.2, 0.6, 1, 0.3]
        self.ripples = []

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # Create ripple effect
            self.create_ripple(touch.pos)
            return super().on_touch_down(touch)
        return False

    def create_ripple(self, pos):
        """Create Material Design ripple effect"""
        with self.canvas.after:
            ripple_color = Color(*self.ripple_color)
            # Start small circle that expands
            # Implementation would include proper ripple animation


class FloatingActionButton(ButtonBehavior, BoxLayout):
    """Material Design Floating Action Button with shadow"""

    def __init__(self, icon='plus', **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(56), dp(56))
        self.icon = icon

        # Add shadow and circular background
        with self.canvas.before:
            # Shadow layers for depth
            Color(0, 0, 0, 0.1)
            self.shadow3 = RoundedRectangle(radius=[dp(28)], size=self.size)
            Color(0, 0, 0, 0.08)
            self.shadow2 = RoundedRectangle(radius=[dp(28)], size=self.size)
            Color(0, 0, 0, 0.05)
            self.shadow1 = RoundedRectangle(radius=[dp(28)], size=self.size)

            # Main button
            Color(0.13, 0.39, 0.65, 1)  # Primary color
            self.bg = RoundedRectangle(radius=[dp(28)], size=self.size)

        self.bind(pos=self._update_graphics, size=self._update_graphics)

    def _update_graphics(self, *args):
        # Update all shadow and background positions
        for i, shadow in enumerate([self.shadow1, self.shadow2, self.shadow3], 1):
            offset = i * 2
            shadow.pos = (self.x - offset, self.y - offset)
            shadow.size = (self.width + offset*2, self.height + offset*2)

        self.bg.pos = self.pos
        self.bg.size = self.size


class ProgressCard(BoxLayout):
    """Modern progress card with animated indicators"""

    def __init__(self, title, current_value, max_value, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.title = title
        self.current_value = current_value
        self.max_value = max_value

        # Card background
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg = RoundedRectangle(radius=[dp(8)])
            self.bind(pos=self._update_bg, size=self._update_bg)

        # Title
        self.add_widget(Label(
            text=title,
            font_size='16sp',
            color=[0.2, 0.2, 0.2, 1],
            size_hint_y=None,
            height=dp(30)
        ))

        # Progress bar container
        progress_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            padding=[dp(10), 0]
        )

        # Create animated progress bar
        self.progress_bar = self._create_progress_bar()
        progress_container.add_widget(self.progress_bar)

        # Value label
        progress_container.add_widget(Label(
            text=f"{current_value}/{max_value}",
            font_size='14sp',
            size_hint_x=None,
            width=dp(60)
        ))

        self.add_widget(progress_container)

        # Animate progress on creation
        Clock.schedule_once(self._animate_progress, 0.5)

    def _create_progress_bar(self):
        """Create custom animated progress bar"""
        container = BoxLayout(size_hint_y=None, height=dp(8))

        with container.canvas:
            # Background
            Color(0.9, 0.9, 0.9, 1)
            self.progress_bg = RoundedRectangle(radius=[dp(4)])

            # Progress fill
            Color(0.13, 0.39, 0.65, 1)
            self.progress_fill = RoundedRectangle(radius=[dp(4)])

        container.bind(pos=self._update_progress_bar, size=self._update_progress_bar)
        return container

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def _update_progress_bar(self, *args):
        self.progress_bg.pos = self.progress_bar.pos
        self.progress_bg.size = self.progress_bar.size

        # Calculate progress width
        progress_percent = self.current_value / self.max_value if self.max_value > 0 else 0
        progress_width = self.progress_bar.width * progress_percent

        self.progress_fill.pos = self.progress_bar.pos
        self.progress_fill.size = (progress_width, self.progress_bar.height)

    def _animate_progress(self, dt):
        """Animate progress bar loading"""
        # Start with 0 width and animate to actual value
        self.progress_fill.size = (0, self.progress_bar.height)

        progress_percent = self.current_value / self.max_value if self.max_value > 0 else 0
        target_width = self.progress_bar.width * progress_percent

        # Animate the width
        anim = Animation(
            size=(target_width, self.progress_bar.height),
            duration=1.0,
            transition='out_cubic'
        )
        anim.start(self.progress_fill)


class MetricCard(BoxLayout):
    """Enhanced metric display card with trend indicators"""

    def __init__(self, title, value, trend=None, icon=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.size_hint_y = None
        self.height = dp(120)
        self.spacing = dp(8)
        self.padding = [dp(16), dp(12)]

        # Card styling
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg = RoundedRectangle(radius=[dp(8)])
            # Subtle border
            Color(0.9, 0.9, 0.9, 1)
            self.border = Line(rounded_rectangle=[0, 0, 0, 0, dp(8)], width=1)
            self.bind(pos=self._update_graphics, size=self._update_graphics)

        # Header with icon and trend
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(24))

        # Title
        header.add_widget(Label(
            text=title,
            font_size='12sp',
            color=[0.5, 0.5, 0.5, 1],
            halign='left',
            valign='middle'
        ))

        # Trend indicator
        if trend:
            trend_color = [0.2, 0.7, 0.3, 1] if trend > 0 else [0.8, 0.2, 0.2, 1]
            trend_symbol = "↗" if trend > 0 else "↘"
            header.add_widget(Label(
                text=f"{trend_symbol} {abs(trend):.1f}%",
                font_size='10sp',
                color=trend_color,
                size_hint_x=None,
                width=dp(60)
            ))

        self.add_widget(header)

        # Value
        self.add_widget(Label(
            text=str(value),
            font_size='28sp',
            color=[0.1, 0.1, 0.1, 1],
            bold=True,
            halign='center'
        ))

    def _update_graphics(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.border.rounded_rectangle = [*self.pos, *self.size, dp(8)]


class ActionSheet(FloatLayout):
    """Material Design bottom action sheet"""

    def __init__(self, actions=None, **kwargs):
        super().__init__(**kwargs)
        self.actions = actions or []

        # Overlay
        with self.canvas.before:
            Color(0, 0, 0, 0.5)
            self.overlay = RoundedRectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_overlay, pos=self._update_overlay)

        # Action sheet container
        self.sheet = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(len(self.actions) * 56 + 32),
            pos_hint={'center_x': 0.5, 'y': 0}
        )

        # Sheet background
        with self.sheet.canvas.before:
            Color(1, 1, 1, 1)
            self.sheet_bg = RoundedRectangle(
                radius=[dp(16), dp(16), 0, 0],
                size=self.sheet.size,
                pos=self.sheet.pos
            )

        self.sheet.bind(pos=self._update_sheet_bg, size=self._update_sheet_bg)

        # Add actions
        for action in self.actions:
            self._add_action_item(action)

        self.add_widget(self.sheet)

        # Animate in
        self.sheet.y = -self.sheet.height
        Animation(y=0, duration=0.3, transition='out_cubic').start(self.sheet)

    def _add_action_item(self, action):
        """Add an action item to the sheet"""
        item = Button(
            text=action.get('text', ''),
            size_hint_y=None,
            height=dp(56),
            background_color=[0, 0, 0, 0],  # Transparent
            color=[0.2, 0.2, 0.2, 1]
        )

        if 'callback' in action:
            item.bind(on_press=lambda x: action['callback']())

        self.sheet.add_widget(item)

    def _update_overlay(self, *args):
        self.overlay.size = self.size
        self.overlay.pos = self.pos

    def _update_sheet_bg(self, *args):
        self.sheet_bg.size = self.sheet.size
        self.sheet_bg.pos = self.sheet.pos

    def dismiss(self):
        """Animate out and remove"""
        def remove_self(animation, widget):
            if self.parent:
                self.parent.remove_widget(self)

        anim = Animation(y=-self.sheet.height, duration=0.3, transition='in_cubic')
        anim.bind(on_complete=remove_self)
        anim.start(self.sheet)


# Integration helpers for your existing components
class EnhancedUIHelpers:
    """Helper methods to enhance your existing UI components"""

    @staticmethod
    def add_hover_effect(widget, hover_color=None):
        """Add hover effect to any widget"""
        if not hover_color:
            hover_color = [0.95, 0.95, 0.95, 1]

        original_color = widget.background_color if hasattr(widget, 'background_color') else [1, 1, 1, 1]

        def on_enter(*args):
            if hasattr(widget, 'background_color'):
                widget.background_color = hover_color

        def on_leave(*args):
            if hasattr(widget, 'background_color'):
                widget.background_color = original_color

        widget.bind(on_enter=on_enter, on_leave=on_leave)

    @staticmethod
    def add_ripple_to_button(button):
        """Add ripple effect to existing buttons"""
        # Implementation would add ripple effect to your existing buttons
        pass

    @staticmethod
    def create_loading_indicator():
        """Create modern loading spinner"""
        from kivy.uix.widget import Widget
        from kivy.graphics import PushMatrix, PopMatrix, Rotate

        spinner = Widget(size_hint=(None, None), size=(dp(40), dp(40)))

        with spinner.canvas:
            PushMatrix()
            spinner.rotation = Rotate(angle=0, origin=spinner.center)
            Color(0.13, 0.39, 0.65, 1)
            # Add spinning arc or circle
            PopMatrix()

        # Animate rotation
        def animate_spin(dt):
            spinner.rotation.angle += 6
            spinner.rotation.origin = spinner.center

        Clock.schedule_interval(animate_spin, 1/60)
        return spinner
