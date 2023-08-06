# bailam_api

## installation 

!pip install git+https://gitlab.com/kamouno/bailam_api@develop


## Usage 

### learning from dataframe dfa to dataframe dfb:
ba = bailamapi.BailamAPI("test_from_python", dfa, dfb,token="security token")

or 

ba = bailamapi.BailamAPI()

### apply the mapping 

ba.map(dfa)

### get the code of the function 

get_mapping_function_code()
 

### for more you can find sample jupyter notebook in the samples folder

### you can also find a running example at : https://colab.research.google.com/drive/1s_ZrBOgPZvZdj5_ieFp8VUm5oeiqBFe4?usp=sharing