package main

import (
	"fmt"
	"log"
	"math/rand"
	"net"
	"net/http"
	"runtime"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

var hist = prometheus.NewHistogramVec(prometheus.HistogramOpts{
	Namespace: "test",
	Name:      "working_time_exported",
	Help:      "",
	Buckets:   []float64{100, 1000, 10000, 100000, 1000000, 10000000},
}, []string{"lang", "method", "langVersion"})

type myhandler struct {
}

func (m myhandler) ServeHTTP(writer http.ResponseWriter, request *http.Request) {
	metricValue := (rand.Intn(90000-50) + 50) * 1000
	ststsDString := fmt.Sprintf(
		"working_time#method=%s,lang=%s,langVersion=%s:%d|ms",
		request.Method,
		"golang",
		runtime.Version(),
		metricValue,
	)
	writer.Header().Add("value", fmt.Sprintf("%d", metricValue))
	hist.With(map[string]string{
		"lang":        "golang",
		"method":      request.Method,
		"langVersion": runtime.Version(),
	}).Observe(float64(metricValue))
	con.Write([]byte(ststsDString))
	writer.Write([]byte("ok"))
}

var con net.Conn

func main() {
	var err error
	con, err = net.Dial("udp", "statsd-exporter:9125")
	if err != nil {
		log.Fatal("failed to start statsd connection: %s", err)
	}

	prometheus.DefaultRegisterer.Register(hist)
	// Register the metrics handler.
	http.Handle("/metrics", promhttp.Handler())
	http.Handle("/", promhttp.InstrumentMetricHandler(prometheus.DefaultRegisterer, myhandler{}))

	// Start the HTTP server.
	log.Fatal(http.ListenAndServe(":8080", nil))
}
