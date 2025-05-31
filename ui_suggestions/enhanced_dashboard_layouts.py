#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Dashboard Layout Suggestions
Modern layout patterns for your existing enhanced dashboard
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.clock import Clock


class ResponsiveDashboard(BoxLayout):
    """Responsive dashboard that adapts to different screen sizes"""

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.bind(size=self._adapt_layout)

    def _adapt_layout(self, *args):
        """Adapt layout based on screen width"""
        if self.width < dp(768):  # Mobile layout
            self._build_mobile_layout()
        elif self.width < dp(1024):  # Tablet layout
            self._build_tablet_layout()
        else:  # Desktop layout
            self._build_desktop_layout()

    def _build_mobile_layout(self):
        """Single column layout for mobile"""
        # Stack all components vertically
        pass

    def _build_tablet_layout(self):
        """Two column layout for tablets"""
        # 2x2 grid or side-by-side panels
        pass

    def _build_desktop_layout(self):
        """Full desktop layout with sidebar"""
        # Multi-column with sidebar
        pass


class ModernStatsGrid(GridLayout):
    """Enhanced stats grid with consistent spacing and animations"""

    def __init__(self, stats_data=None, **kwargs):
        super().__init__(**kwargs)
        self.stats_data = stats_data or []
        self.cols = self._calculate_columns()
        self.spacing = dp(16)
        self.padding = [dp(16), dp(16)]

        self.bind(width=self._recalculate_columns)

    def _calculate_columns(self):
        """Calculate optimal number of columns based on width"""
        if self.width < dp(600):
            return 1
        elif self.width < dp(900):
            return 2
        elif self.width < dp(1200):
            return 3
        else:
            return 4

    def _recalculate_columns(self, *args):
        """Recalculate columns when width changes"""
        new_cols = self._calculate_columns()
        if new_cols != self.cols:
            self.cols = new_cols
            self._rebuild_stats()

    def _rebuild_stats(self):
        """Rebuild stats cards with new column layout"""
        self.clear_widgets()
        for stat in self.stats_data:
            # Create enhanced stat card
            card = self._create_stat_card(stat)
            self.add_widget(card)

    def _create_stat_card(self, stat_data):
        """Create an enhanced statistics card"""
        card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(140),
            spacing=dp(8),
            padding=[dp(16), dp(12)]
        )

        # Card background with gradient effect
        with card.canvas.before:
            Color(*stat_data.get('color', [0.13, 0.39, 0.65, 1]))
            card.bg = RoundedRectangle(radius=[dp(12)])
            card.bind(pos=lambda *x: setattr(card.bg, 'pos', card.pos),
                     size=lambda *x: setattr(card.bg, 'size', card.size))

        # Title
        card.add_widget(Label(
            text=stat_data.get('title', ''),
            font_size='14sp',
            color=[1, 1, 1, 0.8],
            size_hint_y=None,
            height=dp(30)
        ))

        # Value with animation
        value_label = Label(
            text='0',  # Start at 0 for animation
            font_size='32sp',
            color=[1, 1, 1, 1],
            bold=True
        )
        card.add_widget(value_label)

        # Animate value counting up
        Clock.schedule_once(
            lambda dt: self._animate_value(value_label, stat_data.get('value', 0)),
            0.5
        )

        return card

    def _animate_value(self, label, target_value):
        """Animate counter from 0 to target value"""
        def update_counter(dt):
            current = int(label.text) if label.text.isdigit() else 0
            if current < target_value:
                increment = max(1, target_value // 20)  # Animate in ~20 steps
                new_value = min(current + increment, target_value)
                label.text = str(new_value)
                return True  # Continue animation
            return False  # Stop animation

        Clock.schedule_interval(update_counter, 0.05)


class ActivityFeed(ScrollView):
    """Modern activity feed component"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.container = BoxLayout(
            orientation='vertical',
            spacing=dp(8),
            size_hint_y=None,
            padding=[dp(16), dp(8)]
        )
        self.container.bind(minimum_height=self.container.setter('height'))

        self.add_widget(self.container)

    def add_activity(self, activity_data):
        """Add new activity item with slide-in animation"""
        item = self._create_activity_item(activity_data)

        # Start with zero height for slide animation
        item.height = 0
        item.opacity = 0

        self.container.add_widget(item, index=0)  # Add to top

        # Animate in
        Animation(
            height=dp(80),
            opacity=1,
            duration=0.3,
            transition='out_cubic'
        ).start(item)

    def _create_activity_item(self, data):
        """Create individual activity item"""
        item = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(80),
            spacing=dp(12),
            padding=[dp(16), dp(8)]
        )

        # Background with subtle border
        with item.canvas.before:
            Color(1, 1, 1, 1)
            item.bg = RoundedRectangle(radius=[dp(8)])
            Color(0.9, 0.9, 0.9, 1)
            item.border = Line(rounded_rectangle=[0, 0, 0, 0, dp(8)], width=1)
            item.bind(
                pos=lambda *x: [
                    setattr(item.bg, 'pos', item.pos),
                    setattr(item.border, 'rounded_rectangle', [*item.pos, *item.size, dp(8)])
                ],
                size=lambda *x: [
                    setattr(item.bg, 'size', item.size),
                    setattr(item.border, 'rounded_rectangle', [*item.pos, *item.size, dp(8)])
                ]
            )

        # Icon/Avatar placeholder
        icon_container = BoxLayout(
            size_hint_x=None,
            width=dp(48)
        )

        icon = BoxLayout(size_hint=(None, None), size=(dp(40), dp(40)))
        with icon.canvas.before:
            Color(0.13, 0.39, 0.65, 1)
            icon.circle = RoundedRectangle(radius=[dp(20)], size=icon.size, pos=icon.pos)
            icon.bind(pos=lambda *x: setattr(icon.circle, 'pos', icon.pos),
                     size=lambda *x: setattr(icon.circle, 'size', icon.size))

        icon_container.add_widget(icon)
        item.add_widget(icon_container)

        # Content
        content = BoxLayout(orientation='vertical', spacing=dp(4))

        # Title
        content.add_widget(Label(
            text=data.get('title', ''),
            font_size='14sp',
            color=[0.2, 0.2, 0.2, 1],
            halign='left',
            size_hint_y=None,
            height=dp(20)
        ))

        # Description
        content.add_widget(Label(
            text=data.get('description', ''),
            font_size='12sp',
            color=[0.5, 0.5, 0.5, 1],
            halign='left',
            text_size=(None, None)  # Allow text wrapping
        ))

        item.add_widget(content)

        # Timestamp
        item.add_widget(Label(
            text=data.get('time', ''),
            font_size='11sp',
            color=[0.6, 0.6, 0.6, 1],
            size_hint_x=None,
            width=dp(60)
        ))

        return item


class QuickActionsPanel(GridLayout):
    """Enhanced quick actions with improved visual hierarchy"""

    def __init__(self, actions=None, **kwargs):
        super().__init__(**kwargs)
        self.actions = actions or []
        self.cols = 2
        self.spacing = dp(16)
        self.padding = [dp(16), dp(16)]

        self._build_actions()

    def _build_actions(self):
        """Build action cards with modern design"""
        for action in self.actions:
            card = self._create_action_card(action)
            self.add_widget(card)

    def _create_action_card(self, action_data):
        """Create modern action card with hover effects"""
        card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            spacing=dp(8),
            padding=[dp(16), dp(12)]
        )

        # Card styling with subtle gradient
        with card.canvas.before:
            Color(1, 1, 1, 1)
            card.bg = RoundedRectangle(radius=[dp(12)])
            # Border for definition
            Color(0.92, 0.92, 0.92, 1)
            card.border = Line(rounded_rectangle=[0, 0, 0, 0, dp(12)], width=1)
            card.bind(
                pos=lambda *x: [
                    setattr(card.bg, 'pos', card.pos),
                    setattr(card.border, 'rounded_rectangle', [*card.pos, *card.size, dp(12)])
                ],
                size=lambda *x: [
                    setattr(card.bg, 'size', card.size),
                    setattr(card.border, 'rounded_rectangle', [*card.pos, *card.size, dp(12)])
                ]
            )

        # Icon
        icon_color = action_data.get('color', [0.13, 0.39, 0.65, 1])
        icon = BoxLayout(
            size_hint_y=None,
            height=dp(48)
        )
        # Add icon implementation here

        card.add_widget(icon)

        # Title
        card.add_widget(Label(
            text=action_data.get('title', ''),
            font_size='14sp',
            color=[0.2, 0.2, 0.2, 1],
            bold=True,
            halign='center'
        ))

        # Make clickable with subtle feedback
        def on_touch_down(touch):
            if card.collide_point(*touch.pos):
                # Scale animation for press feedback
                Animation(
                    size=(card.width * 0.95, card.height * 0.95),
                    duration=0.1
                ).start(card)

                # Call action
                if 'callback' in action_data:
                    Clock.schedule_once(
                        lambda dt: action_data['callback'](),
                        0.1
                    )

                # Scale back
                Clock.schedule_once(
                    lambda dt: Animation(
                        size=(card.width / 0.95, card.height / 0.95),
                        duration=0.1
                    ).start(card),
                    0.1
                )

                return True
            return False

        card.bind(on_touch_down=on_touch_down)

        return card


class ModernSidebar(BoxLayout):
    """Enhanced sidebar with smooth animations"""

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.size_hint_x = None
        self.width = dp(280)

        # Sidebar background
        with self.canvas.before:
            Color(0.98, 0.98, 0.98, 1)
            self.bg = RoundedRectangle(radius=[0, dp(16), dp(16), 0])
            # Subtle shadow
            Color(0, 0, 0, 0.1)
            self.shadow = RoundedRectangle(radius=[0, dp(16), dp(16), 0])
            self.bind(pos=self._update_bg, size=self._update_bg)

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.shadow.pos = (self.x - dp(4), self.y)
        self.shadow.size = (self.width + dp(4), self.height)

    def slide_in(self):
        """Animate sidebar sliding in"""
        self.x = -self.width  # Start off-screen
        Animation(x=0, duration=0.3, transition='out_cubic').start(self)

    def slide_out(self, callback=None):
        """Animate sidebar sliding out"""
        anim = Animation(x=-self.width, duration=0.3, transition='in_cubic')
        if callback:
            anim.bind(on_complete=callback)
        anim.start(self)


# Layout integration suggestions for your existing components
class DashboardLayoutSuggestions:
    """Suggestions for integrating these components with your existing dashboard"""

    @staticmethod
    def enhance_existing_dashboard(dashboard_screen):
        """Enhance your existing DashboardScreen with these new components"""

        # 1. Replace existing stats grid with responsive version
        # if hasattr(dashboard_screen, 'stats_container'):
        #     dashboard_screen.stats_container = ModernStatsGrid(stats_data=your_stats)

        # 2. Add activity feed to sidebar
        # if hasattr(dashboard_screen, 'sidebar'):
        #     activity_feed = ActivityFeed()
        #     dashboard_screen.sidebar.add_widget(activity_feed)

        # 3. Enhance quick actions
        # if hasattr(dashboard_screen, 'actions_grid'):
        #     enhanced_actions = QuickActionsPanel(actions=your_actions)
        #     dashboard_screen.replace_widget(dashboard_screen.actions_grid, enhanced_actions)

        pass

    @staticmethod
    def create_modern_header():
        """Create modern header with proper visual hierarchy"""
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(64),
            spacing=dp(16),
            padding=[dp(24), dp(8)]
        )

        # Add modern styling
        with header.canvas.before:
            Color(1, 1, 1, 1)
            header.bg = RoundedRectangle(radius=[0, 0, dp(16), dp(16)])
            Color(0.95, 0.95, 0.95, 1)
            header.border = Line(rounded_rectangle=[0, 0, 0, 0, dp(16)], width=1)
            header.bind(
                pos=lambda *x: [
                    setattr(header.bg, 'pos', header.pos),
                    setattr(header.border, 'rounded_rectangle', [*header.pos, *header.size, dp(16)])
                ],
                size=lambda *x: [
                    setattr(header.bg, 'size', header.size),
                    setattr(header.border, 'rounded_rectangle', [*header.pos, *header.size, dp(16)])
                ]
            )

        return header
