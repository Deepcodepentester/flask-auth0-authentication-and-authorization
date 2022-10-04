import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''




@app.route('/drinks')
def get_drinks():
        try:
            categories = Drink.query.all()
            drinks=[question.short() for question in categories]
            return jsonify({
                "success": True,
                "drinks": drinks
                
            })
             
            
        except:
            abort(422)
        
@app.route('/h')
def header():
    # print(json.loads('{"color": "string", "name":"string", "parts":"number"}'))
    r = json.dumps([{"color": "string", "name":"string", "parts":"number"}])
    #return 'Access Granted'   
    # category = Drink.query.get(3)
    # category.delete()
    e=[{"color": "string", "name":"string", "parts":"number"},{"color": "string",
     "name":"string", "parts":"number"}]
    # categories = Drink.query.all()
    # formated_questions=[question.short() for question in categories]
    drink = Drink(title='req_title', recipe=r)
    drink.insert()
    # print(json.loads(category.recipe))
    # return jsonify({
    #             'questions':category.long(),
                
    #         })
    return 'Access Granted'           
        


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''








@app.route('/drinks-detail')
@requires_auth("get:drinks-detail")
def get_drinks_detail(payload):
        try:
            categories = Drink.query.all()
            drinks=[question.short() for question in categories]
            return jsonify({
                "success": True,
                 "drinks": drinks
                
                
            })
             
            
        except:
            abort(422)      


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''






@app.route('/drinks',methods=['POST'])
@requires_auth('post:drinks')
def post_drinks_detail(payload):
        try:
            body= request.get_json()
            title = body.get("title", None)
            r = body.get("recipe", None)
            #curl -d '{"title":"value","recipe":{"color": "string", "name":"string", "parts":"number"}}' -H "Content-Type: application/json" -X POST http://localhost:5000/drinks-detail
            

            rbody = json.dumps([r])
            drink = Drink(title=title, recipe=rbody)
            drink.insert()
            return jsonify({
                "success": True,
                 "drinks": drink.short()
                
                
            })
             
            
        except:
            abort(422) 




'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@app.route('/d')
#@cross_origin(headers=["Content-Type","Authorization"])
@requires_auth("get:drinks-detail")
def patch_drink(payload ):
    return 'access granted'



@app.route('/drinks/<int:id>',methods=['PATCH'])
#@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth("patch:drinks")
def patch_drinks(payload,id):
        try:
            body= request.get_json()
            title = body.get("title", None)
            r = body.get("recipe", None)
            drink = Drink.query.get(id)
            #curl -d '{"title":"value1"}' -H "Content-Type: application/json" -X PATCH http://localhost:5000/drinks/6
            

            rbody = json.dumps([r])
            #drink = Drink(title=title, recipe=rbody)
            drink.title = title
            drink.update()
            return jsonify({
                "success": True,
                 "drinks": drink.short()
                
                
            })
             
            
        except:
            abort(404) 
 


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''




@app.route('/drinks/<int:id>',methods=['DELETE'])
@requires_auth("delete:drinks'")
def delete_drinks(payload,id):
        try:
           
            drink = Drink.query.get(id)
            #curl  -X DELETE http://localhost:5000/drinks/6
            

            
            drink.delete()
            return jsonify({
                "success": True,
                 "drinks": id
                
                
            })
             
            
        except:
            abort(404)



# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(404)
def not_found(error):
        return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

   

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "bad request"}), 400


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
