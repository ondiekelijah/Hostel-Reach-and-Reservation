# Populating database tables

from yourapp import User

new_user = User('user', 'user@gmail.com')
db.session.add(new_user)
db.session.commit()

# Deleting a record

db.session.delete(new_user)
db.session.commit()

# Reverse an commit

db.session.rollback()

# Fetching data

# Getting user by primary key

user_by_id = User.query.get(1)

# Fetching all users using get()

users = User.query.get()

# Handling None
# This will raise 404 errors instead of returning None

user_by_id = User.query.get_or_404()
users = User.query.order_by(User.id.desc()).first_or_404()

# Adding a description to a 404 response

user = User.query.filter_by(username=username).first_or_404(description='No data!')

# Selecting a bunch of users/record by a more complex expression

users = User.query.filter(User.email.endswith('@hotmail.com')).all()




# Limiting users

limited_user = User.query.limit(1).all()



# Query a table and get results of specific column(s)

users = User.query.with_entities(User.email,User.age).first() 
users = User.query.with_entities(User.email,User.age).all()

# Ordering users by something

users = User.query.order_by(User.id.desc()).all()
users = User.query.order_by(User.id.asc()).all()

rooms = Room.query.filter_by(status='Vacant').order_by(Room.id.desc()).all()
rooms = Room.query.filter_by(status='Vacant').order_by(Room.id.desc()).count()



# pagination

page = request.args.get("page", 1, type=int)

posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)

trending = (
	Post.query.filter(Post.views >= 1000)
	    .order_by(Post.date_posted.desc())
	    .paginate(page=page, per_page=10)
	)

# Text search

keyword = request.form.get('search-query')
posts = Post.query.filter(or_(Post.title.ilike(f'%{keyword}%'), Post.body.ilike(f'%{keyword}%'))).all()