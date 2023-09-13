package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"os"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/joho/godotenv"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var (
	collection *mongo.Collection
)

type Item struct {
	ID      primitive.ObjectID       `json:"oid" bson:"_id"`
	UserId  string                   `json:"userId" bson:"userId"`
	Columns []map[string]interface{} `json:"columns" bson:"columns"`
}

type InsertColumnRequest struct {
	ColumnName string                 `json:"columnName"`
	CardName   string                 `json:"cardName"`
	NewItem    map[string]interface{} `json:"newItem"`
}

type UpdateColumnRequest struct {
	ColumnName    string                   `json:"columnName"`
	NewItemsOrder []map[string]interface{} `json:"newItemsOrder"`
}

type DeleteItemRequest struct {
	ColumnName string `json:"columnName"`
	ItemId     int    `json:"itemId"`
	ItemName   string `json:"itemName"`
}

func init() {
	if err := godotenv.Load(); err != nil {
		fmt.Println("Error loading .env file")
		return
	}

	driver := os.Getenv("MONGODB_DRIVER")
	username := os.Getenv("MONGODB_USERNAME")
	password := os.Getenv("MONGODB_PASSWORD")
	cluster := os.Getenv("MONGODB_CLUSTER")

	uri := driver + username + ":" +
		url.QueryEscape(password) + "@" + cluster

	clientOptions := options.Client().ApplyURI(uri)
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	client, err := mongo.Connect(ctx, clientOptions)

	if err != nil {
		log.Fatal("Failed to connect to MongoDB: ", err)
	}

	// confirm connection
	err = client.Ping(ctx, nil)
	if err != nil {
		log.Fatal("Failed to connect to MongoDB: ", err)
	}
	log.Println("Connected to MongoDB!")

	collection = client.Database("chores").Collection("users")
}

func main() {
	app := fiber.New()

	// CORS middleware
	app.Use(cors.New(cors.Config{
		AllowOrigins: "http://localhost:5173",
		AllowHeaders: "Origin, Content-Type, Accept",
	}))

	// Define routes
	app.Get("/hello", func(c *fiber.Ctx) error { return c.SendString("Hello, World 👋!") })
	app.Get("/items", readItems)
	app.Put("/items/insert", createItem)
	app.Put("/items/update", updateItems)
	app.Delete("/items", deleteItem)

	// Start the server
	log.Fatal(app.Listen(":80"))
}

func readItems(c *fiber.Ctx) error {
	log.Println("readItems called")

	items := []Item{}
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	cursor, err := collection.Find(ctx, bson.M{})
	if err != nil {
		log.Println(err)
		return c.Status(http.StatusInternalServerError).JSON(fiber.Map{"error": "Internal server error"})
	}
	defer cursor.Close(ctx)

	for cursor.Next(ctx) {
		var item Item
		if err := cursor.Decode(&item); err != nil {
			log.Println(err)
			return c.Status(http.StatusInternalServerError).JSON(fiber.Map{"error": "Internal server error"})
		}
		items = append(items, item)
	}

	log.Println("Items returned successfully")
	return c.JSON(items)
}

func createItem(c *fiber.Ctx) error {
	log.Println("createItem called")

	var request InsertColumnRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(http.StatusBadRequest).JSON(fiber.Map{"error": "Invalid request data"})
	}

	if request.CardName == "" || request.NewItem == nil || request.ColumnName == "" {
		return c.Status(http.StatusUnprocessableEntity).JSON(fiber.Map{"error": "Invalid request data"})
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	filter := bson.M{"name": request.ColumnName}
	update := bson.M{"$push": bson.M{"items": bson.M{"$each": []interface{}{request.NewItem}, "$position": 0}}}

	log.Println(filter)
	log.Println(update)

	_, err := collection.UpdateOne(ctx, filter, update)
	if err != nil {
		log.Println(err)
		return c.Status(http.StatusInternalServerError).JSON(fiber.Map{"error": "Internal server error"})
	}

	log.Println("Item inserted successfully")
	return c.JSON(fiber.Map{"message": "Item inserted successfully"})
}

func updateItems(c *fiber.Ctx) error {
	log.Println("updateItems called")
	var request UpdateColumnRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(http.StatusBadRequest).JSON(fiber.Map{"error": "Invalid request data"})
	}

	if request.ColumnName == "" {
		return c.Status(http.StatusUnprocessableEntity).JSON(fiber.Map{"error": "Invalid request data"})
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	filter := bson.M{"name": request.ColumnName}
	update := bson.M{"$set": bson.M{"items": request.NewItemsOrder}}

	log.Println(filter)
	log.Println(update)

	_, err := collection.UpdateOne(ctx, filter, update)
	if err != nil {
		log.Println(err)
		return c.Status(http.StatusInternalServerError).JSON(fiber.Map{"error": "Internal server error"})
	}

	log.Println("Items updated successfully")
	return c.JSON(fiber.Map{"message": "Items updated successfully"})
}

func deleteItem(c *fiber.Ctx) error {
	log.Println("deleteItem called")

	var request DeleteItemRequest
	if err := c.BodyParser(&request); err != nil {
		return c.Status(http.StatusBadRequest).JSON(fiber.Map{"error": "Invalid request data"})
	}

	log.Println("Item to be deleted:", request.ItemName)

	if request.ColumnName == "" || request.ItemId == 0 {
		return c.Status(http.StatusUnprocessableEntity).JSON(fiber.Map{"error": "Invalid request data"})
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	filter := bson.M{
		"name":       request.ColumnName,
		"items.name": request.ItemName,
	}

	update := bson.M{"$pull": bson.M{"items": bson.M{"id": request.ItemId}}}

	log.Println(filter)

	_, err := collection.UpdateOne(ctx, filter, update)
	if err != nil {
		log.Println(err)
		return c.Status(http.StatusInternalServerError).JSON(fiber.Map{"error": "Internal server error"})
	}

	log.Println("Item deleted successfully")
	return c.JSON(fiber.Map{"message": "Item deleted successfully"})
}
