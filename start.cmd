@echo off
if not defined TAG (
    set TAG=1
    start wt -p "Windows PowerShell" %0
    exit
)

cd Z:
cd  Z:\User\Projects\Guojiadong\Projects\bulk-ice\RDF\bin\py
echo %cd%
python rdf.py