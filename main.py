from UiController import uiController
from Services.zoomService import ZoomService
from Core.lessonConfiguration import LessonConfiguration as lc

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uiController.run()
    ZoomService(lc.get_lesson()['link']).join()
    print('Hi')


