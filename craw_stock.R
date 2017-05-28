library(RSelenium)
library(rvest)
library(stringr)
library(XML)
library(jsonlite)
#If you run this script the second time i.e. automative browser opened, don't copy the following two command
rd<-rsDriver()
remDr<-rd$client

#Construct the url for search news
news<-NULL
for (i in 1:50) {
url <- "http://www.aastocks.com/tc/stocks/analysis/stock-aafn/"
search <- code[i]
url <- paste(url,search,"/0/hk-stock-news/1",sep = "")
#Connect to Selenium server and use its webdriver for building automative browser

#Navigate the browser to the url of new searching page
links<-NULL
remDr$navigate(url)
  doc <- read_html(remDr$getPageSource()[[1]])
  doc<-htmlParse(doc)
  links<-xpathSApply(doc, "//a[@class='h6']",xmlGetAttr, 'href')
  links<-paste("http://www.aastocks.com",links,sep="")
  links<-links[1:5]
  title<-xpathSApply(doc, "//a[@class='h6']",xmlValue)
  title<-title[1:5]
  text<-xpathSApply(doc, "//div[@class='newscontent2 mcFont2  font15 lettersp2 ']",xmlValue)
  text<-text[1:5]
  image<-xpathSApply(doc, "//div[@class='content_box']//img",xmlGetAttr, 'src')
  image<-image[lapply(image,function(x) length(grep("bannerid",x,value=FALSE))) == 0]
  image<-image[1:5]
  time<-xpathSApply(doc, "//div[@class='newstime2']",xmlValue)
  time<-time[1:5]
  temp<-data.frame(code[i],title,time,text,image,links)
  news<-rbind(news,temp)
}
json<-toJSON(news, pretty=TRUE)
write(json,"~/Desktop/news.json")