# Postit-idea-board
Webflade som udstiller små postit notes. Postit notes indsendes via X-Flow formular til endpoint /api/push, og kræver værdierne "email" samt "data". Data udstilles på webfladen.

ser ud til der er pvc i den her i forhold til kithosting
https://github.com/Randers-Kommune-Digitalisering/kithosting-randers-kommune-apps/blob/0bc3600ccc8ac97a9a1dcb4de6be0dcde0b4e79a/postit-idea-board/values.yaml#L38

    extraVolumes:
      idea-board-db: |
        persistentVolumeClaim:
          claimName: idea-board-db

vurder i henhold til issue #215 hvad der skal gøres med den