# INCItox

The application is available at this [link](https://incitox.streamlit.app/)

## PROJECT GOALS:
- Streamlining the research of toxicological values of molecules found in cosmetic products
- Retrieving and displaying unstructured data present in reputable sources such as [CIR]([https://](https://www.cir-safety.org/)), [PubChem](https://pubchem.ncbi.nlm.nih.gov/) or [ECHA](https://www.echa.europa.eu/)
- Main focus are values of *NOAEL* and *LD50*

## EXECUTION:

### *CIR*:
> A majority of the ingredients present in this data source have a dedicated page in which all sources are listed with a link to their pdf. We navigated the site and extracted the NOAEL and LD50 values present in
> each of the available pdfs trough a regular expression. These data are then organized in a json for each ingredient and saved in a cloud instance of *MongoDB*

### *PubChem*:
> Most of the data of our interest present in this datasource come from another source named *HSDB*, which is available as a JSON file trough an http request. We scanned this JSON and updated exisisting records
> of ingredients already in our database with the new data or created new records when there wasn't a correspondence in our database.

## Streamlit interface:

The way in which people can access the data we collected is trough a web interface built using the framework *streamlit*.

The interface is extremely simple, there's only a selectbox in the center of the screen from which you can choose the name of one of the ingredients present in our database.\
Once an ingredient is selected, two columns will appear underneath the selectbox.

In the left one, if data extracted from *CIR* are available there will be a line indicating name, link and date of publication of the paper analized. Beneath it two buttons for the two metrics we looked for,
by clicking them a table with the values and contexts of the selected metric will appear.

The right column will simply display all LD50 values and associated sources of the selected molecule if they are present in the HSDB.

## Creators:
- [DrMaruki](https://github.com/DrMaruki97)
- [giul-it](https://github.com/giul-it)
 
