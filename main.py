import PySimpleGUI as simpleGui
from PyPDF2 import PdfFileMerger
from datetime import datetime
from PIL import Image
import os

list_of_files = []


def merge_files_in(dir, destination_file_name):
    merger = PdfFileMerger()
    input_docs = []
    try:
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

        output = open(dir + f'/{destination_file_name}.pdf', 'wb')
        merger.write(output)
        merger.close()
    except Exception as merger_error:
        print('Line 38' + str(merger_error))
        raise Exception
    finally:
        for i in input_docs:
            i.close()
        files_in_dir = os.listdir(dir)
        for f in files_in_dir:
            if f.startswith('tmp-juntei-pdf-img'):
                os.remove(dir + f'/{f}')


simpleGui.theme('DarkAmber')  # Add a touch of color
# All the stuff inside your window.


layout = [[simpleGui.Menu([['Ajuda', 'Sobre']], tearoff=False, pad=(200, 1))],
          [simpleGui.Input(enable_events=True, key='InputFiles', visible=False, disabled=True),
           simpleGui.FilesBrowse(button_text='Add Arquivo', target='InputFiles'),
           simpleGui.Button('Remover Arquivo', disabled=True, key='RemoverBtn', enable_events=True),
           simpleGui.Input(enable_events=True, key='DestinationFolder', visible=False, disabled=True),
           simpleGui.FolderBrowse(button_text='Juntar Arquivos', disabled=True, key='JuntarBtn',
                                  target='DestinationFolder')],
          [simpleGui.Text('Digite abaixo o nome do arquivo PDF que será gerado:')],
          [simpleGui.Input(enable_events=True, key='InputNameOfFile', disabled=True, expand_x=True)],
          [simpleGui.Listbox(values=list_of_files, key='ListOfFiles', enable_events=True,
                             auto_size_text=True, expand_x=True, expand_y=True, size=(60, 20))]]

# Create the Window
window = simpleGui.Window('Juntei PDF\'s!', layout, resizable=True)


def control_of_fire_btns():
    if len(list_of_files) > 1:
        window['JuntarBtn'].update(disabled=False)
        window['InputNameOfFile'].update(disabled=False)
        window['RemoverBtn'].update(disabled=False)
    elif len(list_of_files) == 1:
        window['JuntarBtn'].update(disabled=True)
        window['InputNameOfFile'].update(disabled=True)
        window['RemoverBtn'].update(disabled=False)
    else:
        window['JuntarBtn'].update(disabled=True)
        window['InputNameOfFile'].update(disabled=True)
        window['RemoverBtn'].update(disabled=True)


def get_name_of_merged_file():
    if not values['InputNameOfFile'] or values['InputNameOfFile'] == '':
        now = datetime.now()
        return now.strftime("%d-%m-%Y %H%M%S")

    return values['InputNameOfFile']


# Event Loop to process "events" and get the "values" of the inputs
while True:
    try:
        event, values = window.read()
        if event == simpleGui.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break

        if event == 'Sobre':
            window.disappear()
            simpleGui.popup('Sobre esse programa', 'Versão 1.1',
                            "Copyright \u00A9 " + str(datetime.now().year) + " Armando T. Del Col " +
                            "<atdc.codemaster@gmail.com>",
                            'PySimpleGUI Version', simpleGui.version, grab_anywhere=True, title='Sobre')
            window.reappear()

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
            destination_folder = values['DestinationFolder']
            name_of_file = get_name_of_merged_file()
            if destination_folder != '':
                merge_files_in(destination_folder, name_of_file)
                list_of_files.clear()
                window['ListOfFiles'].update(list_of_files)
                control_of_fire_btns()
                window['InputNameOfFile'].update('')
                window['DestinationFolder'].update('')
                simpleGui.popup(
                    "Arquivos combinados com sucesso!\n" +
                    "Novo arquivo gerado:\n" +
                    f"{destination_folder}/{name_of_file}.pdf",
                    title="SUCESSO!"
                )
    except Exception as e:
        print(e)
        simpleGui.popup("Erro inesperado, contate o desenvovledor!", title="ERROR")

window.close()
