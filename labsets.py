from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

# Создаем объект дисплея
display, start_display, add_menu, add_function_to_menu = init_display()

# Создаем куб размером 10 на 10
cube = BRepPrimAPI_MakeBox(10, 10, 10).Shape()

# Добавляем куб на дисплей
display.DisplayShape(cube)

# Запускаем отображение
start_display()