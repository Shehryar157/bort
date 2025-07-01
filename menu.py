import pygame, pygame.locals as pl
from speech import speak
from soundsystem import soundsystem

ss = soundsystem.get_instance()
class menu:
 def __init__(self):
  self.menu_choices = []

 def add_item(self, item):
  self.menu_choices.append(item)

 def reset(self):
  self.menu_choices = []
  # Other reset settings go here

 def run(self, intromsg="hello"):
  choice = -1
  speak(intromsg)
  while True:
   for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
     if event.key == pl.K_UP:
      if choice > 0:
       ss.play(file="ui/click.ogg", volume=70, pan=25)
       choice -= 1
       speak(self.menu_choices[choice])
      else:
       ss.play(file="ui/edge.ogg", volume=70, pan=0)
       speak(self.menu_choices[choice])
     if event.key == pl.K_DOWN:
      if choice < len(self.menu_choices) - 1:
       ss.play(file="ui/click.ogg", volume=70, pan=0)
       choice += 1
       speak(self.menu_choices[choice])
      else:
       ss.play(file="ui/edge.ogg", volume=70, pan=0)
       speak(self.menu_choices[choice])
     if event.key == pl.K_RETURN:
      ss.play(file="ui/confirm.ogg", volume=70, pan=0)
      return choice
