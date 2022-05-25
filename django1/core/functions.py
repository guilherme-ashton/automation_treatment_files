"""import lxml.etree as ET
import pandas as pd
import re
from .forms import UploadFileForm
from pandas import DataFrame
from pylogix import PLC
import os
import xml.etree.cElementTree as ETc


# Funções

 #Inserir linhas em DataFrame
def inserir_linha(idx, df, df_inserir):
    dfA = df.iloc[:idx, ]
    dfB = df.iloc[idx:, ]

    df = dfA.append(df_inserir).append(dfB).reset_index(drop=True)

    return df

 #Funções do Interlock
def ledados(tag):
    with PLC() as comm:
        comm.ProcessorSlot = 0
        comm.IPAddress = '192.168.15.109'
        valor = comm.Read(tag)
        return valor.Value


def lestring(tag):
    with PLC() as comm:
        comm.ProcessorSlot = 0
        comm.IPAddress = '192.168.15.109'
        str_len = comm.Read(tag + '.LEN').Value
        if str_len > 0:
            data = comm.Read(tag + '.DATA[0]', int(str_len)).Value
            value = ''.join([chr(d) for d in data])
        else:
            value = ' '
        ret = value
        print(value)


def escrevestring(TAG, txt):
    with PLC() as comm:
        comm.ProcessorSlot = 0
        comm.IPAddress = '192.168.15.109'
        stuff = [ord(c) for c in txt]
        comm.Write(TAG + '.LEN', len(stuff))
        comm.Write(TAG + '.DATA[0]', stuff)


def escreve(TAG, valor):
    with PLC() as comm:
        comm.ProcessorSlot = 0
        comm.IPAddress = '192.168.15.109'
        comm.Write(TAG, valor)

def gera_root(self):
    settings_dir = os.path.dirname(__file__)
    PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
    PLC_FOLDER = os.path.join(PROJECT_ROOT, 'PLC/')
    plcs = os.listdir(PLC_FOLDER)
    lista_root=[]
    for plc in plcs:
        mydoc = ET.parse(PLC_FOLDER + plc)
        root = mydoc.getroot()
        lista_root.append([str(plc),root])
    return lista_root, plcs

def tipotag(tag, root):
    # Acha todas as rotinas do tipo Function Block Diagram (FBD)
    for elem in root.findall(".//Tags/Tag[@Name='" + tag + "']"):
        return elem.attrib['DataType']

def tagsTela(self =None, xml_teste=None):
    print(xml_teste, type(xml_teste))
    #settings_dir = os.path.dirname(__file__)
    #PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
    #TELAS_FOLDER = os.path.join(PROJECT_ROOT, 'Telas/')
    #telas = os.listdir(TELAS_FOLDER)
    telas =
    #print (type(telas))
    listafinalTela = []
    for i in range(len(telas)):
        listaTela = []
        tela = (telas[i])
        #print(tela)
        try:  # Se possivel, ele compila as telas do xml
            tree = ET.parse(TELAS_FOLDER + tela)
            root = tree.getroot()
            sequence = ET.tostring(root, encoding='utf8').decode('utf8')
            #print(sequence)
            j = re.compile(r'(parameter name=\"#102\"*.*value=\")\{(.*)\::\[(.*)](.*\w)')
            for match in j.finditer(sequence):
                match4 = match.group(4)
                match3 = match.group(3)
                match2 = match.group(2)
                listafinalTela.append([match3,match4,match2,tela])
            #listafinalTela.append(listaTela)
        except:
            pass
    df=pd.DataFrame(listafinalTela)
    #print(df)
    df.to_excel("Telas_tag.xlsx")
    return listafinalTela, telas

def intlk(blocoescrita):
    listaroot,plcs=gera_root(self=1)
    listafinal = []
    for root in listaroot:
        for sheet in root[1].findall(f".//Program/Routines/Routine[@Type='FBD']/FBDContent/Sheet/AddOnInstruction[@Name='{blocoescrita}']/.."):
            for bloco in sheet.findall(f".//AddOnInstruction[@Name='{blocoescrita}']"):
                tagname = bloco.attrib["Operand"].replace(f'_{blocoescrita}', '')
                listafinal.append([tagname, tipotag(tagname, root[1]), ""])
                for wire in sheet.xpath(f"./*[contains(@ToParam ,'Inp_Intlk')][not(contains(@ToParam,'StatusOk'))]"):
                    # print(wire.attrib["ToParam"])
                    for IRef in sheet.findall("./IRef[@ID='" + wire.attrib['FromID'] + "']"):
                        tag = IRef.attrib["Operand"].split(".")[0]
                        listafinal.append([tag, tipotag(tag, root[1]), tagname])
    df=pd.DataFrame(listafinal)
    df.to_excel('tagsplcs.xlsx')
    return listafinal , len(listafinal), plcs

def cruza_tags(telas,plcs):
    listafinal=[]
    for i in telas:
        check = False
        for j in plcs:
            if i[1] == j[2]:
                check == True
                listafinal.append([j[2],j[0],i[0],i[2],i[3],j[1]])
        if check == False:
            for j in plcs:
                if i[1] == j[0]:
                    listafinal.append(['',i[1],i[0],i[2],i[3],j[1]])
    df=pd.DataFrame(listafinal, columns=['Bloco','Tag', 'Topico', 'Diretorio', 'Tela', 'Tipo'])
    drop=["BOOL", "P_Logic", "P_Intlk", "TIMER","REAL","DINT"]
    drop.extend(["CLX_CommValor","P_GateStandAlone","P_PF755_Inp"])
    df=df[~df['Tipo'].isin(drop)]
    df.drop_duplicates(keep='first', inplace=True)
    df.reset_index().drop(["index"], axis=1)
    df.to_excel("intlk.xlsx")
    return df

def gera_lvu(self):
    listafinal, rnglst, plcs = intlk("C_IntlkProtect")
    listatelas, telas = tagsTela(self=1)
    df = (cruza_tags(listatelas, listafinal))
    lista_tag = df['Tag'].tolist()
    lista_topico = df['Topico'].tolist()
    lista_diretorio = df['Diretorio'].tolist()
    lista_tela = df['Tela'].tolist()
    lista_tipo = df['Tipo'].tolist()

    ### Encontra no primeiro dataframe as telas e relaciona com as tags do PLC e insere em um DataFrame ###

    for i in range(len(lista_tag)):
        for j in range(rnglst):
            var = listafinal[j][0]
            if (lista_tag[i] == var):
                varTop = listafinal[j][2]
                # print(var)
                # print(varTop)
                if (lista_topico[i] == varTop):
                    # print('encontrou')
                    # print(listafinal[j][1])
                    df_inserido = {'Tag': [listafinal[j][1]],
                                   'Topico': [lista_topico[i]],
                                   'Diretorio': [lista_diretorio[i]],
                                   'Tela': [lista_tela[i]],
                                   'Tipo': [listafinal[j][4]]}
                    df_inserido = pd.DataFrame(data=df_inserido)
                    df = inserir_linha(i + 1, df, df_inserido)

                    ### Remove do Dataframe completo os valores repetidos e deixa só o primeiro encontrado
    result_df = df.drop_duplicates(subset=['Tag'], keep='first')
    ### Mostra os valores duplicados do DataFrame ###
    ### dff = df[df.duplicated(keep=False)] ###
    result_df.to_csv("CSV.csv", index=False)

    ### Usado para escrever no arquivo lvu ###
    lista_tag1 = result_df['Tag'].tolist()
    lista_topico1 = result_df['Topico'].tolist()
    lista_diretorio1 = result_df['Diretorio'].tolist()
    lista_tela1 = result_df['Tela'].tolist()
    lista_tipo1 = result_df['Tipo'].tolist()

    ### Lista valores unicos dos tipos ###
    provisorio = set(lista_tipo1)
    lista_tipo2 = list(provisorio)

    projeto = 'sinter4/Dados_1'
    arquivo = open('alarmes.lvu', 'w')

    texto = ('<?xml version="1.0" encoding="utf-8"?>' + '\n' +
             '<LogixViewProject LastUpdated="09/06/2021 16:34:44" LVU_Version="Version 6.3.0.18">' + '\n' +
             '  <ControllerFiles CurrentControllerName="' + str(plcs[0]) + '">' + '\n')

    arquivo.write(texto)
    arquivo.close()

    arquivo = open('alarmes.lvu', 'a')
    for i in range(len(plcs)):
        # plcSemPlant = (plcs[5]).split('_')[0]
        texto = ('    <ControllerFile ControllerName="' + str(plcs[i]).replace(".L5X","") + '" XmlFileName="">' + '\n' +
                 '      <LogixDescFormat>' + '\n' +
                 '        <NumberOfFields>1</NumberOfFields>' + '\n' +
                 '        <Delimiter>vbCrLf</Delimiter>' + '\n' +
                 '        <TagLabelFields>0</TagLabelFields>' + '\n' +
                 '        <TagDescFields>1</TagDescFields>' + '\n' +
                 '        <TagEngineeringUnitFields>0</TagEngineeringUnitFields>' + '\n' +
                 '        <FieldDescriptors>' + '\n' +
                 '          <Field Name="1" Descriptor="" />' + '\n' +
                 '        </FieldDescriptors>' + '\n' +
                 '      </LogixDescFormat>' + '\n' +
                 '    </ControllerFile>' + '\n')
        arquivo.write(texto)

    texto = ('  </ControllerFiles>' + '\n' + '  <HMI>' + '\n')

    arquivo.write(texto)

    for i in range(len(plcs)):
        texto = ('    <ControllerHMI ControllerName="' + str(plcs[i]).replace(".L5X","") + '">' + '\n' +
                 '      <DataServerAreaName>' + projeto + '</DataServerAreaName>' + '\n' +
                 '      <DataServerShortcutName>' + str(plcs[i]).replace(".L5X","").split('_PlantPAx')[0] + '</DataServerShortcutName>' + '\n' +
                 '      <DataServerName>Dados_1</DataServerName>' + '\n' +
                 '      <HmiServerName>HMI projects</HmiServerName>' + '\n' +
                 '      <HmiServerAreaName>' + projeto.split('/')[0] + '</HmiServerAreaName>' + '\n' +
                 '      <HmiDir>C:\Documents and Settings\All Users\Documents\RSView Enterprise\SE\HMI projects</HmiDir>' + '\n' +
                 '      <HmiGfxFileDir />' + '\n' +
                 '      <HmiParFileDir>C:\Documents and Settings\All Users\Documents\RSView Enterprise\SE\HMI projects\PAR</HmiParFileDir>' + '\n' +
                 '      <HmiGfxXmlFileDir>C:\Documents and Settings\All Users\Documents\RSView Enterprise\SE\HMI projects\gfx_xml</HmiGfxXmlFileDir>' + '\n' +
                 '      <LogixViewHmiXmlFileName>C:\Documents and Settings\All Users\Documents\RSView Enterprise\SE\HMI projects\LogixView_HMI projects.xml</LogixViewHmiXmlFileName>' + '\n' +
                 '      <ApplicationName>Sinter4_PlantPAx</ApplicationName>' + '\n' +
                 '      <ProductType>RSViewDistributed</ProductType>' + '\n' +
                 '      <HmiLibraryName>EmptyHmiLibrary</HmiLibraryName>' + '\n' +
                 '    </ControllerHMI>' + '\n')
        arquivo.write(texto)

    texto = ('  </HMI>' + '\n' +
             '  <ProjectObjects>' + '\n' +
             '    <ProjectObject Name="Alarmes_CSN" DisplayName="Alarmes_CSN" Desc="" ParentName="" NodeIndex="0">' + '\n' +
             '      <IsSharing>False</IsSharing>' + '\n' +
             '      <SharedBaseObjectName />' + '\n' +
             '      <CanBeShared>False</CanBeShared>' + '\n' +
             '      <Tags />' + '\n' +
             '    </ProjectObject>' + '\n')

    arquivo.write(texto)
    arquivo.close()

    arquivo = open('alarmes.lvu', 'a')
    for i in range(len(telas)):
        tela = telas[i]
        texto = ('    <ProjectObject Name="' + str(tela) + '" DisplayName="' + str(tela).replace("(sinter-3) ","").replace(".xml","").replace(" ","_") + '" Desc="" ParentName="Alarmes_CSN" NodeIndex="' + str(i) + '">' + '\n' +
                 '      <IsSharing>False</IsSharing>' + '\n' +
                 '      <SharedBaseObjectName />' + '\n' +
                 '      <CanBeShared>False</CanBeShared>' + '\n' +
                 '      <Tags />' + '\n' +
                 '    </ProjectObject>' + '\n')
        arquivo.write(texto)
    arquivo.close()

    arquivo = open('alarmes.lvu', 'a')

    # Percorre Todas as Telas
    for i in range(len(telas)):
        tela = telas[i]
        # Percorre todos os tipos listado unicos
        for j in range(len(lista_tipo2)):
            tipo = lista_tipo2[j]
            texto = ('    <ProjectObject Name="' + str(tipo) + str(i) + '" DisplayName="' + str(tipo) + str(i) + '" Desc="" ParentName="' + str(tela) + '" NodeIndex="' + str(j) + '">' +
                     '\n' + '      <IsSharing>False</IsSharing>' + '\n' +
                     '      <SharedBaseObjectName />' + '\n' +
                     '      <CanBeShared>False</CanBeShared>' + '\n' +
                     '      <Tags>' + '\n')
            arquivo.write(texto)
            # Percorrendo todo o dataframe
            for x in range(len(lista_tag1)):
                if (tela == lista_tela1[x] and tipo == lista_tipo1[x]):
                    texto = ('        <Tag FullLogixTagAddress="' + lista_topico1[x] + '.' + lista_tag1[x] + '" LogixController= "' + lista_topico1[x] + '" LogixName="' + lista_tag1[x] + '" LogixScope="" />' + '\n')
                    arquivo.write(texto)
            texto = ('      </Tags>' + '\n' + '    </ProjectObject>' + '\n')
            arquivo.write(texto)
    arquivo.close()

    arquivo = open('alarmes.lvu', 'a')
    texto = ('  </ProjectObjects>' + '\n' + '  <ProjectObjects_LogixCodes />' + '\n' +
             '<ProjectObjects_HmiFiles>' + '\n' +
             '  <ProjectObject_HmiFiles Name="Alarmes_CSN">' + '\n' +
             '    <GfxFiles />' + '\n' +
             '    <GfxXmlFiles />' + '\n' +
             '  </ProjectObject_HmiFiles>' + '\n')
    arquivo.write(texto)

    for i in range(len(telas)):
        texto = ('  <ProjectObject_HmiFiles Name="' + str(telas[i]) + '">' + '\n' +
                 '    <GfxFiles />' + '\n' +
                 '    <GfxXmlFiles />' + '\n' +
                 '  </ProjectObject_HmiFiles>' + '\n')
        arquivo.write(texto)
        i += 1

    texto = ('  </ProjectObjects_HmiFiles>' + '\n'
                                              '  <AlarmServers>' + '\n')
    arquivo.write(texto)
    arquivo.close()

    arquivo = open('alarmes.lvu', 'a')
    texto = ('    <AlarmServer Name="Alarmes_1" Desc="" LastAeXmlFileCreatedUsingAlarmGroups="False">' + '\n'
                                                                                                         '      <Controllers>' + '\n')
    arquivo.write(texto)

    for i in range(len(plcs)):
        texto = ('        <Controller ControllerName="' + str(plcs[i]).replace(".L5X","") + '" />' + '\n')
        arquivo.write(texto)
        i += 1

    texto = ('      </Controllers>' + '\n'
                                      '      <Folders />' + '\n'
                                                            '   </AlarmServer>' + '\n'
                                                                                  '  </AlarmServers>' + '\n'
                                                                                                        '  <HistorianServers />' + '\n'
                                                                                                                                   '</LogixViewProject>')

    arquivo.write(texto)
    arquivo.close()
gera_lvu(self=1)"""""