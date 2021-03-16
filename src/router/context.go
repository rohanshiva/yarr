package router

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"
)

type Context struct {
	Req   *http.Request
	Out   http.ResponseWriter

	Vars  map[string]string

	chain []Handler
	index int
}

func (c *Context) Next() {
	c.index++
	c.chain[c.index](c)
}

func (c *Context) JSON(status int, data interface{}) {
	body, err := json.Marshal(data)
	if err != nil {
		log.Fatal(err)
	}
	c.Out.WriteHeader(status)
	c.Out.Header().Set("Content-Type", "application/json; charset=utf-8")
	c.Out.Write(body)
	c.Out.Write([]byte("\n"))
}

func (c *Context) VarInt64(key string) (int64, error) {
	if val, ok := c.Vars[key]; ok {
		return strconv.ParseInt(val, 10, 64)
	}
	return 0, fmt.Errorf("no such var: %s", key)
}

func (c *Context) QueryInt64(key string) (int64, error) {
	query := c.Req.URL.Query()
	return strconv.ParseInt(query.Get("page"), 10, 64)
}
