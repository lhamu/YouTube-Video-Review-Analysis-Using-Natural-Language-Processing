from apiclient.discovery import build
from comment_threads import get_comment_threads
from search import youtube_search
# arguments to be passed to build function
DEVELOPER_KEY = "*******************"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# creating youtube resource object for interacting with API
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

i=0
result=[]

if __name__ == "__main__":
    id1=youtube_search("Justin Bieber Baby")
    print len(id1)
    for vid_id in id1:
        result.append(get_comment_threads(youtube,vid_id))
        fileName="file"+str(i)+".txt"
        f=open(fileName,'w+')
        for j in range(0,len(result[i])):
            f.write(result[i][j].encode('ascii','ignore'))

        payload={'id':search_result["id"]["videoId"],'part':'contentDetails,statistics,snippet','key':DEVELOPER_KEY}
        1=requests.Session().get('http://www.googleapis.com/youtube/v3/videos',params=payload)
        print 1
        f.close()
        i+=1
    
