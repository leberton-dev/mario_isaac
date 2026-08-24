from .scene import Scene

class SceneManager:
    def __init__(self) -> None:
        self._scenes: list[Scene] = []

    @property
    def current_scene(self) -> Scene:
        return self._scenes[len(self._scenes) - 1]

    def add(self, scene: Scene) -> None:
        self._scenes.append(scene)

    def pop(self) -> None:
        _ = self._scenes.pop()

