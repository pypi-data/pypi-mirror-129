# DevDeck - OBS

OBS controls for [DevDeck](https://github.com/jamesridgway/devdeck).

In this example, you can change scenes in OBS.


## Installing
Simplify install *DevDeck - OBS* into the same python environment that you have installed DevDeck.

    pip install devdeck-obs

You can then update your DevDeck configuration to use decks and controls from this package.

## Configuration

Example configuration:
```yaml
decks:
  - serial_number: "ABC123"
    name: 'devdeck.decks.single_page_deck_controller.SinglePageDeckController'
    settings:
      controls:
        - key: 3
          name: devdeck_obs.obs_control.OBSControl
          settings:
            scene_name: Webcam
            emoji: 'camera'
        - key: 8
          name: devdeck_obs.obs_control.OBSControl
          settings:
            scene_name: Desktop
            emoji: 'desktop_computer'
        - key: 13
          name: devdeck_obs.obs_control.OBSControl
          settings:
            scene_name: AFK
            emoji: 'zzz'
```



## Credentials
Currently this does not use a username and password to access the OBS websocket. This may change in future, but the default will always be `'':''`.
