import PySimpleGUI as simpleGui
from PyPDF2 import PdfFileMerger
from datetime import datetime
from PIL import Image
import os

list_of_files = []


def merge_files_in(dir):
    merger = PdfFileMerger()
    input_docs = []

    for f in list_of_files:
        if f.endswith('.pdf'):
            input_doc = open(f, 'rb')
        else:
            image = Image.open(f)
            im1 = image.convert('RGB')
            now = datetime.now()
            img_file_name = f'tmp-juntei-pdf-img-{now.strftime("%d-%m-%Y %H%M%S%f")}.pdf'
            im1.save(dir + f'/{img_file_name}')
            input_doc = open(dir + f'/{img_file_name}', 'rb')
            image.close()
        merger.append(input_doc)
        input_docs.append(input_doc)

    now = datetime.now()
    output = open(dir + f'/{now.strftime("%d-%m-%Y %H%M%S")}.pdf', 'wb')
    merger.write(output)
    merger.close()
    for i in input_docs:
        i.close()
    files_in_dir = os.listdir(dir)
    for f in files_in_dir:
        if f.startswith('tmp-juntei-pdf-img'):
            os.remove(dir + f'/{f}')


simpleGui.theme('DarkAmber')  # Add a touch of color
# All the stuff inside your window.


layout = [[simpleGui.Input(enable_events=True, key='InputFiles', visible=False, disabled=True),
           simpleGui.FilesBrowse(button_text='Add PDF', target='InputFiles'),
           simpleGui.Button('Remover PDF', disabled=True, key='RemoverBtn', enable_events=True),
           simpleGui.Input(enable_events=True, key='DestinationFolder', visible=False, disabled=True),
           simpleGui.FolderBrowse(button_text='Juntar PDF\'s', disabled=True, key='JuntarBtn',
                                  target='DestinationFolder')],
          [simpleGui.Listbox(values=list_of_files, size=(60, 20), key='ListOfFiles', enable_events=True,
                             auto_size_text=True)]]

# Create the Window
window = simpleGui.Window('Juntei PDF\'s!', layout, resizable=True)


def control_of_fire_btns():
    if len(list_of_files) > 1:
        window['JuntarBtn'].update(disabled=False)
        window['RemoverBtn'].update(disabled=False)
    elif len(list_of_files) == 1:
        window['JuntarBtn'].update(disabled=True)
        window['RemoverBtn'].update(disabled=False)
    else:
        window['JuntarBtn'].update(disabled=True)
        window['RemoverBtn'].update(disabled=True)


# Event Loop to process "events" and get the "values" of the inputs
while True:
    try:
        event, values = window.read()
        if event == simpleGui.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break

        if event == 'InputFiles':
            if values['InputFiles'] != '':
                files = values['InputFiles'].split(';')
                files = list(filter(lambda x: x.endswith('.pdf') or
                                              x.endswith('.jpg') or
                                              x.endswith('.jpeg') or
                                              x.endswith('.png'),
                                    files))
                for file in files:
                    list_of_files.append(file)
                    window['ListOfFiles'].update(list_of_files)
                window['InputFiles'].update('')
                control_of_fire_btns()

        if event == 'RemoverBtn':
            if len(values['ListOfFiles']) > 0:
                list_of_files.remove(values['ListOfFiles'][0])
                window['ListOfFiles'].update(list_of_files)
            control_of_fire_btns()

        if event == 'DestinationFolder':
            merge_files_in(values['DestinationFolder'])
            list_of_files.clear()
            window['ListOfFiles'].update(list_of_files)
            control_of_fire_btns()
            simpleGui.popup("Arquivos combinados com sucesso!")
    except Exception:
        simpleGui.popup("Erro inesperado!")

window.close()
