import json
class Config():
    def __init__(self) -> None:
        
        self.boilerplate = {
            "pixela_user" : None,
            "pixela_token" : None,
            "pixela_graph" : [
                {"graph_id" : None,
                "graph_name" : None}]
        }
        pass

    def reset(self) -> None:
        with open("data\config.json","w") as file:
            json.dump(self.boilerplate,file,indent=4,sort_keys= True)
        return
    def read_value(self,key:str=None):
        with open("data\config.json","r") as file:
            data = json.load(file)
        if key is None:
            return data
        else:
            return data[key]

    def update_key(self,key:str,value):
        with open("data\config.json","r") as file:
            data = json.load(file)
        data[key] = value
        with open("data\config.json","w") as file:
            json.dump(data,file,indent=4,sort_keys= True)
        return

# Config().reset()
# print(Config().read_value("pixela_user"))
# print(Config().update_key("pixela_user",12))
