# Geotables

Install dependecies
- https://www.ghostscript.com/releases/gsdnld.html

Clone ArcGIS Pro Default Python Environment using Conda
- Open the Python Command Prompt
- Clone the environment: "conda create -n {enter enviroment name}  --clone arcgispro-py3"
- Check to make sure it was properly created in: 
    C:\Users\{YourUserName}\AppData\Local\ESRI\conda\envs
    or
    D:\Profile\{YourUserName}\AppData\Local\ESRI\conda\envs
- Enter the directory of your new environment
- Change to the environment with: "activate {enter enviroment name}"

Install the Camelot Libraries
- After properly creating and changing to the environment, execute the following in your terminal:
    - pip3 install camelot-py[cv] tabula-py


Run the program through Visual Studio

Note: Make sure you fun the program in the Geotables directory so the program can find the PDF file in its directory.