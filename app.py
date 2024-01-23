from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_instagram_profile(username):
    url = f"https://www.instagram.com/{username}/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            meta_description = soup.find("meta", property="og:description")
            meta_image = soup.find("meta", property="og:image")
            meta_title = soup.find("meta", property="og:title")  # Adicionado para extrair o nome completo
            if meta_description and meta_image and meta_title:
                content = meta_description.get("content")
                followers, following, posts = content.split(" - ")[0].split(", ")
                profile_image_url = meta_image.get("content")
                full_name = meta_title.get("content").split(" (@")[0]  # Extrai o nome completo
                return {
                    "username": username,
                    "full_name": full_name,  
                    "followers": followers.split(" ")[0],
                    "following": following.split(" ")[0],
                    "posts": posts.split(" ")[0],
                    "profile_image": profile_image_url
                }
            else:
                return {"error": "Não foi possível encontrar as tags meta"}
        else:
            return {"error": "Resposta HTTP não foi bem-sucedida"}
    except Exception as e:
        return {"error": str(e)}

@app.route('/instagram/<username>', methods=['GET'])
def instagram_profile(username):
    profile_data = get_instagram_profile(username)
    return jsonify(profile_data)

if __name__ == '__main__':
    app.run(debug=True)
