import os
import aiohttp
from aiomultiprocess import Pool
from rdkit import Chem
import asyncio
import uvloop
import re


async def fetch(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    result = await response.text()
    session.close()
    return result
'''
async def download_mol(chembl_id):
    info_url = 'https://www.ebi.ac.uk/chembl/compound/inspect/' + chembl_id
    info_html_content = await fetch(info_url)
    print(info_html_content)
    mol_file = chembl_id + '.mol'
    with open(mol_file,'w') as f:
        f.write(info_html_content)
    
    return
       
'''

async def get_molrengo(chembl_id):
    url = 'https://www.ebi.ac.uk/chembl/compound/inspect/' + chembl_id
    html_content = await fetch(url)
    # print(html_content)
    p = re.compile(r"/chembl/download_helper/getmol/(\d{1,50})'>Download\sMolFile")
    # print(p)
    # p = r"/chembl/download_helper/getmol/(\d{1,50})'>Download\sMolFile"
    m = re.search(p, html_content).group(1)
    # print(m)
    return m
 


async def download_mol(chembl_id):
    molrengo = await get_molrengo(chembl_id)
    print(molrengo)
    ligand_url = 'https://www.ebi.ac.uk/chembl/download_helper/getmol/' + molrengo
    liagnd_info = await fetch(ligand_url)
    mol_file = chembl_id + '.mol'
    with open(mol_file,'w') as f:
        f.write(liagnd_info)
    mol = Chem.MolFromMolFile(mol_file)
    sd_file = chembl_id + '.sdf'
    sd_writer = Chem.SDWriter(sd_file)
    sd_writer.write(mol)
    return

async def aiomultipro(func, parmas_list):
    async with Pool(processes = 100) as pool:
        result = await pool.map(func, parmas_list)
    #pool = Pool(processes = 100)
    #result = await pool.map(chembl_download, parmas_list)
    #pool.close()
    return result
    
if __name__ == '__main__':
    import datetime
    start = datetime.datetime.now()
    print("The start time is: " + str(start))
    # chembl_id_list = ['CHEMBL3304053']
    chembl_id_list = ['CHEMBL3304053'  ,
                      'CHEMBL3303318'  ,
                      'CHEMBL418052'   ,
                      'CHEMBL167256'   ,
                      'CHEMBL3303571'  ,
                      'CHEMBL3303897'  ,
                      'CHEMBL3303601'  ,
                      'CHEMBL3304015'  ,
                      'CHEMBL3303946'  ,
                      'CHEMBL3303586'  ,
                      'CHEMBL3303359'  ,
                      'CHEMBL3304104'  ,
                      'CHEMBL3303633'  ,
                      'CHEMBL3304169'  ,
                      'CHEMBL3304018'  ,
                      'CHEMBL3276568'  ,
                      'CHEMBL3303378'  ,
                      'CHEMBL3546269'  ,
                      'CHEMBL3303348'  ,
                      'CHEMBL3559072'  ,
                      'CHEMBL1178552'  ,
                      'CHEMBL277041'   ,
                      'CHEMBL3228260'  ,
                      'CHEMBL1183261'  ,
                      'CHEMBL288035'   ,
                      'CHEMBL3392201'  ,
                      'CHEMBL3392202'  ,
                      'CHEMBL34209'    ,
                      'CHEMBL3303361'  ,
                      'CHEMBL3304047'  ,
                      'CHEMBL161318']
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(aiomultipro(download_mol, chembl_id_list))
    # loop.run_until_complete(aiomultipro(get_molrengo, chembl_id_list))
    end = datetime.datetime.now()
    print ("The end time is: " + str(end))
    print("The function run time is : "+str(end - start))