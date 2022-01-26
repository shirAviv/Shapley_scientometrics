"""An example program that uses the elsapy module"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
from pybliometrics.scopus import ScopusSearch
from pybliometrics.scopus import AuthorRetrieval
from pybliometrics.scopus import AbstractRetrieval



import json
# from Bio import Entrez


## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
client = ElsClient(config['apikey'], num_res=500)
client.inst_token = config['insttoken']

# scopus=ScopusSearch('AU-ID(26326340200)', subscriber=True, view="COMPLETE")

ab = AbstractRetrieval('10.1108/AJIM-01-2017-0014', id_type='doi', view='FULL')

# scopus=ScopusSearch('SRCTITLE(Scientometrics) AND REFSRCTITLE(Journal of Informetrics)', subscriber=True, view="COMPLETE")


scopus=ScopusSearch('AFFILCOUNTRY(israel) AND AFFILCOUNTRY(palestine)', view='COMPLETE', facets='subjarea')
# AFFILCOUNTRY(ISRAEL) AND AFFILCOUNTRY(France)
print(scopus.results)
str='(AFFILCOUNTRY(Israel) AND AFFILCOUNTRY(palestine))'
myDocSearch=ElsSearch(str, 'scopus')
myDocSearch.execute(client, get_all=True)
myDocSearch.results


exit(0)
au = AuthorRetrieval(26326340200)

## Author example
# Initialize author with uri
# Initialize author search object and execute search
auth_srch = ElsSearch('authlast(keuskamp)','author')
auth_srch.execute(client)
print ("auth_srch has", len(auth_srch.results), "results.")

exit(0)

# testSearch=ElsSearch('subj=COMP','title')
# testSearch.execute(client, get_all=True)
# exit(0)
# content/serial/title
# str='SRCTITLE(IEEE Transactions on Pattern Analysis and Machine Intelligence) AND PUBYEAR > 2018 '

str='subj=CHEM'
myDocSearch=ElsSearch(str, 'title')
myDocSearch.execute(client, get_all=False)

print(myDocSearch.results)
exit(0)
pii_doc = FullDoc(sd_pii='0181551220301406')
if pii_doc.read(client):
    print("pii_doc.title: ", pii_doc.title)
    pii_doc.write()
else:
    print("Read document failed.")

# str='affil(Public Health and Infection Research Group, Faculty of Health Sciences)'
# myDocSearch=ElsSearch(str, 'affiliation')
# myDocSearch.execute(client, get_all=False)
# myDocSearch.results

str='SRCTITLE(Artifical)'
myDocSearch=ElsSearch(str, 'scopus')
myDocSearch.execute(client, get_all=True)
myDocSearch.results

# doi_doc = FullDoc(doi='10.1016/j.tmaid.2020.101623')
# if doi_doc.read(client):
#     print("doi_doc.title: ", doi_doc.title)
#     doi_doc.write()
# else:
#     print("Read document failed.")
#




## Author example
# Initialize author with uri
my_auth = ElsAuthor(
    uri='https://api.elsevier.com/content/author/author_id/7004367821')
# Read author data, then write to disk
if my_auth.read(client):
    print("my_auth.full_name: ", my_auth.full_name)
    my_auth.write()
else:
    print("Read author failed.")

## Affiliation example
# Initialize affiliation with ID as string
my_aff = ElsAffil(affil_id='60101411')
if my_aff.read(client):
    print("my_aff.name: ", my_aff.name)
    my_aff.write()
else:
    print("Read affiliation failed.")
#
## Scopus (Abtract) document example
# Initialize document with ID as integer
# scp_doc = AbsDoc(scp_id=84872135457)
# if scp_doc.read(client):
#     print("scp_doc.title: ", scp_doc.title)
#     scp_doc.write()
# else:
#     print("Read document failed.")

## ScienceDirect (full-text) document example using PII


## ScienceDirect (full-text) document example using DOI
doi_doc = FullDoc(doi='10.1016/S1525-1578(10)60571-5')
if doi_doc.read(client):
    print("doi_doc.title: ", doi_doc.title)
    doi_doc.write()
else:
    print("Read document failed.")

## Load list of documents from the API into affilation and author objects.
# Since a document list is retrieved for 25 entries at a time, this is
#  a potentially lenghty operation - hence the prompt.
print("Load documents (Y/N)?")
s = input('--> ')

if (s == "y" or s == "Y"):

    ## Read all documents for example author, then write to disk
    if my_auth.read_docs(client):
        print("my_auth.doc_list has " + str(len(my_auth.doc_list)) + " items.")
        my_auth.write_docs()
    else:
        print("Read docs for author failed.")

    ## Read all documents for example affiliation, then write to disk
    if my_aff.read_docs(client):
        print("my_aff.doc_list has " + str(len(my_aff.doc_list)) + " items.")
        my_aff.write_docs()
    else:
        print("Read docs for affiliation failed.")

## Initialize author search object and execute search
auth_srch = ElsSearch('authlast(keuskamp)', 'author')
auth_srch.execute(client)
print("auth_srch has", len(auth_srch.results), "results.")

## Initialize affiliation search object and execute search
aff_srch = ElsSearch('affil(amsterdam)', 'affiliation')
aff_srch.execute(client)
print("aff_srch has", len(aff_srch.results), "results.")

## Initialize doc search object using Scopus and execute search, retrieving
#   all results
doc_srch = ElsSearch("AFFIL(dartmouth) AND AUTHOR-NAME(lewis) AND PUBYEAR > 2011", 'scopus')
doc_srch.execute(client, get_all=True)
print("doc_srch has", len(doc_srch.results), "results.")

## Initialize doc search object using ScienceDirect and execute search,
#   retrieving all results
doc_srch = ElsSearch("star trek vs star wars", 'sciencedirect')
doc_srch.execute(client, get_all=False)
print("doc_srch has", len(doc_srch.results), "results.")