from flask import Flask ,jsonify,request,abort

app = Flask(__name__)
# in memory database
items=[
    {'id':1,"name":"Laptop","price":5200},
    {'id':2,"name":"phone","price":6700}
]

@app.route("/")
def home():
    return {"message":"Welcome to flask REST api"}

#get all the items 
@app.route("/items" , methods = ["GET"])
def get_items():
    return jsonify(items)

#get item by id
@app.route("/items/<int:itemid>" , methods = ["GET"])
def get_item(itemid):
    for item in items:
        if item['id'] == itemid:
            return jsonify(item)
    abort(404,description="item not found")
#update item
@app.route("/item<int:itemid>", methods=["PUT"])
def updateitem(itemid):
    item = next((i for i in items if i ['id']==itemid),None)
    if item is None:
        abort(404)
    if not request.json:
        abort(404)
    item['name']=request.json.get('name',item['name'])
    item['price']= float(request.json.get('price',item['price']))
    return jsonify(item)
#delete item
@app.route("/item<int:itemid>", methods=["DELETE"])
def deleteitems(itemid):
    global items
    items = [i for i in items if i['id'] != itemid]
    return jsonify({"message":"item deleted"})
#create item

@app.route("/items",methods=["POST"])
def createitem():
    data = request.get_json()
    if not data or "name" not in data or "price" not in data:
        abort(400,description="invalid input")
    newId = items[-1]['id']+1 if items else 1
    item = {
        'id':newId,
        'name':request.json['name'],
        'price':float(request.json['price'])
    }
    items.append(item)
    return jsonify(item),201
if __name__ == "__main__":
    app.run(debug=True)