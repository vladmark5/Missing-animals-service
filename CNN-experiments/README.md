### Cropping_dogs
Cropping_dogs.ipynb - Данный скрипт предназначен для детекции одних собак с последующим вырезанием получившихся bounding boxs. Это позволяет избавиться от лишнего фона на изображении и сосредоточить внимание только на фичах собак. Таким образом формируется новый датасет, состоящий только лишь из изображений собак.

### Dogs_hacaton_experiments
Dogs_hacaton_experiments.ipynb - В данном скрипте были проведены эксперименты по обучению нейронной сети для классификации собак на 6 категорий по цветам и длине хвоста.

### Experiments_color
Experiments_color.ipynb - В данном скрипте нейронная сети обучалась классификации собак на 3 класса только по цвету: multicolored, dark, light. Наилучший результат по точности показала Bilinear CNN (76,79% val_accuracy). Данную модель также можно скачать по [ссылке](https://drive.google.com/file/d/1sr_Lln4Sf2n5Nx9CZnXSIip0ElPFxD_g/view?usp=sharing).

### Experiments_tail
Experiments_tail.ipynb - В данном скрипте нейронная сети обучалась классификации собак на 2 класса только по длине хвоста: long, short. Наилучший результат по точности показала Bilinear CNN (64,29% val_accuracy). Данную модель также можно скачать по [ссылке](https://drive.google.com/file/d/14pKHnWMTH-1bq5wkY1RLYhsOhR6tnH45/view?usp=sharing)

### Pipline_for_models
Pipline_for_models.ipynb - В данном скрипте показывается применение выше описанных нейронных сетей в качестве примера. 
