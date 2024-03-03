import requests
import random
from scripts.config import Config
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

class Pixela():
    def __init__(self) -> None:
        self.endpoint = "https://pixe.la/v1/users"
        self.colors = {
            "red": "momiji",
            "green": "shibafu",
            "blue" : "sora",
            "yellow": "ichou",
            "purple": "ajisai",
            "black" : "kuro"
        }
        pass

    def error(self,code:int) -> dict:
        """
            This method provides error information.
            Returns dict.
        """
        return

    def merge(self,*args):
        final_list = []
        return_str = ""
        for arg in args:
            final_list.extend(arg)
        random.shuffle(final_list)    
        while final_list[0].isalpha() == False:
                random.shuffle(final_list)   
        for char in final_list:
            return_str += char
        return return_str
    
    def generate_pixela_info(self) -> dict:
        alphabet = ['a','b','c','d','e',
                    'f','g','h','i','j',
                    'k','l','m','n','o',
                    'p','q','r','s','t',
                    'u','v','w','x','y','z']
        numbers = [0,1,2,3,4,5,6,7,8,9]
        symbols = ['!', '@', '#', '$']
        
        if True: # for token
            total_length = random.randint(8,128)
            rem_length = total_length
            lenght_char = random.randint(5,total_length-3)
            rem_length -= lenght_char
            lenght_num = random.randint(2,rem_length-1)
            rem_length -= lenght_num
            lenght_sym = rem_length
            rem_length -= lenght_sym
            token_list_char = [random.choice(alphabet) for _ in range(lenght_char)]
            token_list_num = [str(random.choice(numbers)) for _ in range(lenght_num)]
            token_list_sym = [random.choice(symbols) for _ in range(lenght_sym)]
            token = self.merge(token_list_char,token_list_num,token_list_sym)

        if True: # for username
            total_length = random.randint(8,32)
            rem_length = total_length
            lenght_char = random.randint(5,total_length-3) 
            rem_length -= lenght_char
            lenght_num = rem_length
            username_list_char = [random.choice(alphabet) for _ in range(lenght_char)]
            username_list_num = [str(random.choice(numbers)) for _ in range(lenght_num)]
            username = self.merge(username_list_char,username_list_num)
        
        if True: # for graph id
            total_length = random.randint(8,16)
            rem_length = total_length
            lenght_char = random.randint(4,total_length-4)
            rem_length -= lenght_char
            lenght_num = rem_length
            id_list_char = [random.choice(alphabet) for _ in range(lenght_char)]
            id_list_num = [str(random.choice(numbers)) for _ in range(lenght_num)]
            graph_id = self.merge(id_list_char,id_list_num)
        return{"X-USER-TOKEN":token,
            "user":username,
            "graph_id":graph_id}

    def create_user(self) -> dict:
        """
            This method generates unique 'X-USER-TOKEN' and 'username' to create a pixe.la account and returns them.\n
            Returns False if any error occur.
        """
        info = self.generate_pixela_info()
        # generate token
        token = info['X-USER-TOKEN']
        # generate username
        username = info['user']
        user_param = {
            "token" : token,
            "username" : username,
            "agreeTermsOfService" : "yes",
            "notMinor" : "yes"
        }
        response = requests.post(url=self.endpoint,json=user_param)
        response.raise_for_status()
        if response.json()['isSuccess']:
            return {
                "X-USER-TOKEN" : token,
                "username": username
            }
        return False

    def create_graph(self,token:str,user:str,name:str,color:str="momiji",timezone:str="Asia/Kathmandu") -> str:
        """
            This method generates unique str:graph-id to create pixe.la graph and returns it.\n
            Returns False if any error occur.
        """
        
        # generate id
        generated_id = self.generate_pixela_info()['graph_id']
        endpoint = self.endpoint + f"/{user}/graphs"
        graph_param = {
            "id" : generated_id,
            "name" : name,
            "unit" : "minutes",
            "type" : "int",
            "color" : color,
            "timezone" : timezone
        }
        graph_header = {
            "X-USER-TOKEN" : token
        }
        response = requests.post(url=endpoint,headers=graph_header,json=graph_param)
        response.raise_for_status()
        if response.json()['isSuccess']:
            return generated_id
        return False

    def plot_pixel(self,token:str,user:str,graph_id:str,date:str,quantity:str) -> bool:
        """
            This method plots a pixel in the graph.\n
            Requires token, user, graph_id, date:yyyyMMdd, quantity.\n
            Returns False if any error occur.
        """
        endpoint = f"{self.endpoint}/{user}/graphs/{graph_id}"
        pixel_params = {
            "date":date,
            "quantity":str(quantity)
        }
        pixel_header = {
            "X-USER-TOKEN" : token
        }
        response = requests.post(url=endpoint,headers=pixel_header,json=pixel_params)
        response.raise_for_status()
        if response.json()['isSuccess']:
            return True
        return False
    
    def get_pixel_data(self,token:str,user:str,graph_id:str,date:str) -> dict:
        """ 
            This method gets quantity data of a pixel in the graph for the provided date.\n
            Requires token, user, graph_id, date:yyyyMMdd.\n
            Returns 'quantity' as 0 if no value was found.
            Returns False if any error occur.
        """
        endpoint = f"{self.endpoint}/{user}/graphs/{graph_id}/{date}"

        pixel_header = {
            "X-USER-TOKEN" : token
        }
        response = requests.get(endpoint,headers=pixel_header)
        try:
            if response.json()['message'] == "Specified pixel not found.":
                return{'quantity': 0}
            if response.json()['isSuccess'] is False:
                return False
        except KeyError:
            pass
        response.raise_for_status()
        
        return {'quantity': float(response.json()['quantity'])}

    def create(self,name:str) -> bool:
            """
                This method creates new user and token for pixela account and creates graph with provided name. And only creates the graph if user already exists.\n
                It updates config file with pixela info.\n
                Returns False if any error occur.
            """
            config = Config()
            if config.read_value()['pixela_user'] is None:
                # create a user
                data = self.create_user()
                # store pixele info in config
                config.update_key("pixela_token",data['X-USER-TOKEN'])
                config.update_key("pixela_user",data['username'])
            # create graph
            if (gen_id:= self.create_graph(config.read_value('pixela_token'),config.read_value('pixela_user'),name)) != False:
                prev_data = config.read_value('pixela_graph')
                prev_data[0] = {
                "graph_id": gen_id,
                "graph_name": name
            }
                config.update_key('pixela_graph',prev_data)

                return True
            return 

    def get_graph_stats(self,user:str,graph_id:str):
        """ 
            This method gets quantity data of a pixel in the graph for the provided date.\n
            Requires token, user, graph_id, date:yyyyMMdd.\n
            Returns 'quantity' as 0 if no value was found.
            Returns False if any error occur.
        """
        endpoint = f"{self.endpoint}/{user}/graphs/{graph_id}/stats"

        
        response = requests.get(endpoint)
        response.raise_for_status()
        
        return response.json()

    def save_graph_svg(self,user:str,graph_id:str) -> None:
        """ 
            Saves new(update) graph svg file.
        """
        
        endpoint = f"{self.endpoint}/{user}/graphs/{graph_id}"

        response = requests.get(url=endpoint)
        response.raise_for_status()
        svg = response.text
        with open("data\graph.svg","w") as svg_file:
            svg_file.write(svg)
        drawing = svg2rlg('data\graph.svg')
        renderPM.drawToFile(drawing, "data\graph.png", "PNG")
        return

    def edit_svg(self):
        
        
        return