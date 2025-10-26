from collections import ChainMap

default_settings: dict[str, str | bool] ={
    'theme' :'Light,',
    'language' : 'Egnlish',
    'notfications' : True,
}


user_preferences: dict[str, str | bool] ={
      'theme' :'Dark',
      'notfications' : False,  
}



preferences: ChainMap [str, str | bool] =ChainMap(user_preferences, default_settings)

print(f'{user_preferences= }')
print(f'{default_settings= }')
print(f'{preferences= }')
print(f'{preferences['theme']= }')

