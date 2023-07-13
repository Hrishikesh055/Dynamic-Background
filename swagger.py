{
  "openapi": "3.0.0",
  "info": {
    "title": "Dynamic Background API",
    "version": "1.0"
  },
  "servers": [
    {
      "url": "http://localhost:5000/background"
    }
  ],
  "paths": {
    "/background": {
      "post": {
        "security": [
          {
            "ApiKeyAuth": []
          }
        ],
        "requestBody": {
          "description": "contains the url of the image that needs to be overlayed over the background.",
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "required": [
                  "url"
                ],
                "properties": {
                  "url": {
                    "type": "string",
                    "example": "https://images.theconversation.com/files/133674/original/image-20160810-11853-1iw2v38.jpg?ixlib=rb-1.1.0&q=45&auto=format&w=1200&h=1200.0&fit=crop"
                  },
                  "background_url": {
                    "type": "string",
                    "example": "https://static.vecteezy.com/system/resources/previews/003/031/764/original/blue-wide-background-with-linear-blurred-gradient-free-vector.jpg"
                  }
                }
              }
            }
          }
        },
        "description": "Dynamic Background API generates images with customizable background.",
        "responses": {
          "200": {
            "description": "Returns the customized image.",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "url": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "Returns Error message in case something went wrong",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "message": {
                      "type": "string",
                      "default": "Something went wrong"
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "securitySchemes": {
      "ApiKeyAuth": {
        "type": "apiKey",
        "in": "header",
        "name": "API-key"
      }
    }
  },
  "tags": []
}
