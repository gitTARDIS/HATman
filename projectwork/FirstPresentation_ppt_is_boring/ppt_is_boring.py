from __future__ import division, print_function, unicode_literals

# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


import cocos
from cocos.director import director

import pyglet
from pyglet import font
from pyglet.gl import *
from pyglet.window import key

from cocos.actions import *
from cocos.layer import *
from cocos.scenes.transitions import *
from cocos.sprite import *
from cocos import text

import demo_grid_effects


basepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
pyglet.resource.path.append(basepath)
pyglet.resource.reindex()



class TitleSubTitleLayer(cocos.layer.Layer):

    def __init__(self, title, subtitle, subtitle2=""):
        super(TitleSubTitleLayer, self).__init__()

        x, y = director.get_window_size()

        self.title = text.Label(
            title, (x // 2, y // 2 + 50), font_name='joystix monospace',
            font_size=18, anchor_x='center', anchor_y='center')
        self.add(self.title)

        self.subtitle = text.Label(
            subtitle, (x // 2, y // 2 - 30), font_name='joystix monospace',
            font_size=14, anchor_x='center', anchor_y='center')
        self.add(self.subtitle)

        self.subtitle2 = text.Label(
            subtitle2, (x // 2, y // 2 - 70), font_name='joystix monospace',
            font_size=14, anchor_x='center', anchor_y='center')
        self.add(self.subtitle2)

        bgimage = Sprite('background.jpg')
        bgimage.scale = 0.8
        bgimage.position = x/2, y/2 - 200
        self.add(bgimage, z=-1)

class BulletListLayer(cocos.layer.Layer):

    def __init__(self, title, lines):
        super(BulletListLayer, self).__init__()
        x, y = director.get_window_size()

        self.title = text.Label(
            title, (x // 2, y - 100), font_name='Consolas',
            font_size=46, anchor_x='center', anchor_y='center')
        self.add(self.title)

        start_y = (y // 12) * 8
        font_size = 22
        line_font = font.load('Consolas', font_size)
        tot_height = 0
        max_width = 0
        rendered_lines = []
        step = 40
        i = 0
        for line in lines:
            line_text = text.Label(
                line, (x // 2, y - 185 - step * i), font_name='Consolas',
                font_size=font_size, anchor_x='center', anchor_y='center')
            i += 1
            self.add(line_text)

        bgimage = Sprite('background.jpg')
        bgimage.scale = 0.8
        bgimage.position = x/2, y/2 - 200
        self.add(bgimage, z=-1)

class TransitionControl(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self, scenes, transitions=None):
        super(TransitionControl, self).__init__()

        self.transitions = transitions
        self.scenes = scenes
        for scene in scenes:
            if not self in scene.get_children():
                scene.add(self)

        self.scene_p = 0

    def next_scene(self):
        self.duration = None
        self.scene_p += 1
        if self.scene_p >= len(self.scenes):
            self.scene_p = len(self.scenes) - 1
        else:
            self.transition(self.transitions[self.scene_p % len(self.transitions) - 1])

    def prev_scene(self):
        self.duration = 0.5
        self.scene_p -= 1
        if self.scene_p < 0:
            self.scene_p = 0
        else:
#            self.transition()
            self.transition(self.transitions[self.scene_p % len(self.transitions)])

    def transition(self, transition=None):
        if transition:
            director.replace(transition(
                self.scenes[self.scene_p],
                duration=self.duration
            )
            )
        else:
            director.replace(self.scenes[self.scene_p])

    def on_key_press(self, keyp, mod):
        if keyp in (key.RIGHT,):
            self.next_scene()
        elif keyp in (key.LEFT,):
            self.prev_scene()


class RunScene(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self, target):
        super(RunScene, self).__init__()

        self.target = target

    def on_key_press(self, keyp, mod):
        if keyp in (key.F1,):
            director.push(self.target)

class HelloWorld(cocos.layer.Layer):

    def __init__(self):
        super(HelloWorld, self).__init__()

        # a cocos.text.Label is a wrapper of pyglet.text.Label
        # with the benefit of being a cocosnode
        label = cocos.text.Label('Thank you for your attention!',
                                 font_name='Consolas',
                                 font_size=28,
                                 anchor_x='center', anchor_y='center')

        label.position = 320, 240
        self.add(label)

        # similar to cocos.text.Label, a cocos.sprite.Sprite
        # is a subclass of pyglet.sprite.Sprite with the befits of
        # being a CocosNode.
        sprite = cocos.sprite.Sprite('pacman1.png')
        sprite2 = cocos.sprite.Sprite('pacman2.png')

        # sprite in the center of the screen (default is 0,0)
        sprite.position = 1500, 240
        sprite2.position = 1500, 240

        sprite.scale = 0.4
        sprite2.scale = 0.4

        # add the sprite as a child, but with z=1 (default is z=0).
        # this means that the sprite will be drawn on top of the label
        self.add(sprite, z=1)
        self.add(sprite2, z=1)

        move = MoveTo((300, 240), 6)


        # tell the sprite to scaleback and then scale, and repeat these 2 actions forever
        sprite.do(move)
        sprite2.do(move | Repeat(Blink(1, 0.3)))


if __name__ == "__main__":
    aspect = 1280 / float(800)
    director.init(resizable=True, width=640, height=480)
    director.window.set_fullscreen(True)
    x, y = director.get_window_size()

    pyglet.font.add_directory('..')

    scenes = [

        cocos.scene.Scene(
            TitleSubTitleLayer("Game development with Python", "Team: Bergmann, Halmschlager & Kirchmaier", "Tutor: FH-Prof. Mag. Dr. Wilhelm Zugaj"),
        ),

        cocos.scene.Scene(
            BulletListLayer("Central problem", ["Is it possible to use a high-level", "programming language, that is not", "very common for games, for the", "purpose of developing a", "simple game?"]),
        ),

        cocos.scene.Scene(
            BulletListLayer("Solution -> Python", ["(= mainly used as scripting language)"]),
        ),

        cocos.scene.Scene(
            BulletListLayer("Goal:", ["modified version of the", "classic game Pacman"]),
        ),
        
        cocos.scene.Scene(
            BulletListLayer("Implementation:", ["Using cocos2D, an open source framework", "for game development, cross-platform", "games and apps", "", "Making it possible to play the game in", "multiplayer-mode"]),
        ),

        cocos.scene.Scene(
            BulletListLayer("Steps", ["x Research concerning cocos2D", "and multiplayer possibilities", "x Assessment of OS-requirements", "x Designing a paper prototype", "x Programming & designing the game", "x Final result: Multiplayer Pacman"]),
        ),

        cocos.scene.Scene(
            TitleSubTitleLayer("Presentation made with cocos2D", "(Powerpoint is boring! xD)"),
        ),

        cocos.scene.Scene(
            HelloWorld()
        ),

    ]


    for s in scenes:
            s.add(cocos.layer.ColorLayer(0, 0, 0, 255), z=-1)
    transitions = [None] * (len(scenes) - 1)
    all_t = [
        #'ZoomTransition',

        #'FlipX3DTransition',
        #'FlipY3DTransition', 'FlipAngular3DTransition',

        #'TurnOffTilesTransition',

        #'ShrinkGrowTransition',

        #'FadeTRTransition', 'FadeBLTransition',
        #'FadeUpTransition', 'FadeDownTransition',
        #'ShuffleTransition',

        #'SplitRowsTransition', 'SplitColsTransition',

        #'RotoZoomTransition',

        'FadeTransition',

        #'CornerMoveTransition',
        #'EnvelopeTransition',

        #'MoveInLTransition', 'MoveInRTransition',
        #'MoveInBTransition', 'MoveInTTransition',

        #'JumpZoomTransition',

    ]

    transitions = [getattr(cocos.scenes.transitions, all_t[i % len(all_t)])
                   for i in range(len(scenes) - 1)]

    TransitionControl(scenes, transitions)

    def color_name_scene(name, color):
        return cocos.scene.Scene(
            cocos.layer.ColorLayer(*color).add(
                cocos.text.Label(
                    name, (x / 2, y / 2),
                    font_name='Consolas', font_size=64,
                    anchor_x='center', anchor_y='center'
                )
            )
        )
    director.interpreter_locals["one"] = color_name_scene("one", (255, 0, 0, 255))
    director.interpreter_locals["two"] = color_name_scene("two", (0, 255, 0, 255))
    director.interpreter_locals["three"] = color_name_scene("three", (0, 0, 255, 255))

    director.interpreter_locals["grid_scene"] = demo_grid_effects.start()

    director.run(scenes[0])
