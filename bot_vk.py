import vk
from time import sleep
session=vk.AuthSession(str(6061551),input("Login:"),input("Password:"),scope='messages, wall, friends')
vkapi=vk.API(session,v="5.62")
def forallitems(itemsfunc,func,offs,*itemargs,**itemkwargs):
	ofs=0
	items=itemsfunc(*itemargs,**itemkwargs)
	cont=items["count"]
	requests=0
	while cont>0:
		cont-=len(items["items"])
		for item in items["items"]:
			if not func(item): 
				return None
		if cont>=ofs:
			ofs+=offs
		else:
			ofs=cont
		items=itemsfunc(*itemargs,offset=ofs,**itemkwargs)
		requests+=1
		if requests==3:
			requests=0
			sleep(1)
class Post:
	def __init__(self,oid,pid):
		self.id=str(oid)+"_"+str(pid)
	def __repr__(self):
		return self.id
class User:
	def __init__(self, uid):
		self.id=uid
	def __str__(self):
		return str(self.id)
	def __repr__(self):
		return str(self.id)
	def getfriends(self, count=None):
		friends=[]
		if count==None:
			def f(uid):
				friends.append(User(uid))
		else:
			def f(uid):
				friends.append(User(uid))
				return count>0
				return True
		forallitems(vkapi.friends.get,f,50,id=self.id)
		return friends
	def getwall(self,count=None):
		posts=[]
		cont=count
		if count==None:
			def f(post):
				posts.append(Post(self.id,post["id"]))
				return True
		else:
			def f(post):
				nonlocal cont
				print(cont)
				posts.append(Post(self.id,post["id"]))
				cont-=1
				return cont>0
		forallitems(vkapi.wall.get,f,2,owner_id=self.id,count=5)
		return posts
u=User(171644102)
print(u.getfriends(count=1))
