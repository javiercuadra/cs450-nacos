package main

import (
    "fmt"
    "log"
    "net/http"

    // "github.com/nacos-group/nacos-sdk-go/clients"
    // "github.com/nacos-group/nacos-sdk-go/clients/naming_client"
    // "github.com/nacos-group/nacos-sdk-go/common/constant"
    // "github.com/nacos-group/nacos-sdk-go/vo"
)

func helloHandler(w http.ResponseWriter, r *http.Request) {
    username := r.URL.Query().Get("username")
    if username == "" {
        http.Error(w, "Username is required", http.StatusBadRequest)
        return
    }
    fmt.Fprintf(w, "Hello %s", username)
}

func main() {
    // Nacos configuration
    nacosConfig := NacosConfig{
        ServerIP:   "10.105.10.110", // Replace with your Nacos server IP
        ServerPort: 8848,        // Replace with your Nacos server Port
        Namespace:  "public",    // Replace with your Nacos Namespace
    }

    // Register the Hello service with Nacos
    err := RegisterService(nacosConfig, "HelloService", "127.0.0.1", 8080)
    if err != nil {
        log.Fatalf("Failed to register service: %v", err)
    }

    // Set up the HTTP server and route
    http.HandleFunc("/hello", helloHandler)
    log.Println("Starting Hello Service on port 8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
