#  练习：Web 爬虫

在这个练习中，我们将会使用 Go 的并发特性来并行化一个 Web 爬虫。

修改 `Crawl` 函数来并行地抓取 URL，并且保证不重复。

*提示*：你可以用一个 map 来缓存已经获取的 URL，但是要注意 map 本身并不是并发安全的！

```go
package main 


import(
    "fmt"
    "sync"
)

type Fetcher interface {
    // Fetch 返回 URL 的 body 内容，并且将这个页面上找到的url放到一个slice中
    Fetch(url string)(body string,urls []string,err error)
}

type urlRecord struct {
    v map[string]int  
    mux sync.Mutex      // https://www.jianshu.com/p/9e5554617399
    wg sync.WaitGroup   // 参考 https://juejin.cn/post/7181812988461252667
}

var m = urlRecord{v: make(map[string]int)}

// Crawl 使用 fetcher 从某个 URL 开始递归的爬取页面，直到达到最大深度。
func Crawl(url string, depth int, fetcher Fetcher) {
    // TODO : 并行的抓取 URL.
    // TODO : 不重复抓取页面

    defer m.wg.Done();

    if depth <= 0 {
        return
    }

    m.mux.Lock()
    m.v[url]++
    m.mux.Unlock()
 
    body, urls, err := fetcher.Fetch(url)
    if err != nil {
        fmt.Println(err)
        return
    }
    fmt.Printf("found: %s %q\n", url, body)
    for _, u := range urls {
        m.mux.Lock()
        if _, ok := m.v[u]; !ok {
            m.wg.Add(1)
            go Crawl(u, depth-1, fetcher)
        }
        m.mux.Unlock()
    }
    return

}

func main() {
    m.wg.Add(1)
    Crawl("https://golang.org/", 4, fetcher)
    m.wg.Wait()
}

// fakeFetcher 是返回若干结果的 Fetcher。
type fakeFetcher map[string]*fakeResult


type fakeResult struct {
    body string
    urls []string
}

 
func (f fakeFetcher) Fetch(url string) (string, []string, error) { // 定义 Fetch 方法
    if res, ok := f[url]; ok {
        return res.body, res.urls, nil
    }
    return "", nil, fmt.Errorf("not found: %s", url)
}

// fetcher 是填充后的 fakeFetcher。
var fetcher = fakeFetcher{
    "https://golang.org/": &fakeResult{
        "The Go Programming Language",
        []string{
            "https://golang.org/pkg/",
            "https://golang.org/cmd/",
        },
    },
    "https://golang.org/pkg/": &fakeResult{
        "Packages",
        []string{
            "https://golang.org/",
            "https://golang.org/cmd/",
            "https://golang.org/pkg/fmt/",
            "https://golang.org/pkg/os/",
        },
    },
    "https://golang.org/pkg/fmt/": &fakeResult{
        "Package fmt",
        []string{
            "https://golang.org/",
            "https://golang.org/pkg/",
        },
    },
    "https://golang.org/pkg/os/": &fakeResult{
        "Package os",
        []string{
            "https://golang.org/",
            "https://golang.org/pkg/",
        },
    },
}

```

