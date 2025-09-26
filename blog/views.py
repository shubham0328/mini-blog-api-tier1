from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import in_memory
from .auth import get_user_from_token



# Helper function for safely reading query params (page, page_size)
#It ensures query parameters like page and page_size are valid positive integers, or else returns an error message.
def _parse_positive_int(value, default):    
    """
    Safely parse a positive integer from string-like 'value'.
    Return (int_value, None) on success, or (None, error_message) on failure.
    """
    if value is None:
        return default, None
    try:
        iv = int(value)
    except (ValueError, TypeError):         #value > 0 and positive value (int)
        return None, "must be an integer"
    if iv <= 0:
        return None, "must be a positive integer"
    return iv, None



# Posts list & create post
class PostListCreate(APIView):
    """
    GET: list posts (latest first), supports pagination ?page=&page_size=
    POST: create post (authentication required)
    """

    # lists blog posts in latest-first order and supports safe pagination with page and page_size query parameters.
    def get(self, request):
        # Parse page and page_size safely
        page, err = _parse_positive_int(request.GET.get("page"), 1)     #parse_positive_int -> to ensure they are valid int
        if err:
            return Response({"page": "page {}".format(err)}, status=status.HTTP_400_BAD_REQUEST)

        page_size, err = _parse_positive_int(request.GET.get("page_size"), 5)
        if err:
            return Response({"page_size": "page_size {}".format(err)}, status=status.HTTP_400_BAD_REQUEST)

        # cap page_size to avoid huge results
        MAX_PAGE_SIZE = 100
        if page_size > MAX_PAGE_SIZE:
            return Response({"page_size": f"page_size must be <= {MAX_PAGE_SIZE}"}, status=status.HTTP_400_BAD_REQUEST)

        # latest-first by id (higher id = newer)
        posts_sorted = sorted(in_memory.POSTS, key=lambda x: x["id"], reverse=True) #descending order return posts -> latest-first
        start = (page - 1) * page_size
        end = start + page_size
        return Response(posts_sorted[start:end])
    


    # This method creates a new blog post after verifying the user is authenticated and validating the input. 
    # If everything is valid, the post is stored in memory and returned in the response.
    def post(self, request):    
        # Authentication required
        user = get_user_from_token(request)
        if not user:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data or {}
        title = (data.get("title") or "").strip()   #Reads title from JSON body
        content = (data.get("content") or "").strip()   #Reads content from JSON body

        # Input validation
        if not title:
            return Response({"title": "Title is required."}, status=status.HTTP_400_BAD_REQUEST)
        if len(title) > 200:
            return Response({"title": "Title must be <= 200 characters."}, status=status.HTTP_400_BAD_REQUEST)

        if not content:
            return Response({"content": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)
        if len(content) > 2000:
            return Response({"content": "Content must be <= 2000 characters."}, status=status.HTTP_400_BAD_REQUEST)

        #creates dictionary representing the post
        post = {
            "id": in_memory.get_next_post_id(), #assigns new id
            "title": title, 
            "content": content,
            "author": user["id"], #users id
            "created_at": in_memory._now(), #timestamp
        }
        in_memory.POSTS.append(post)    #save into memory list
        return Response(post, status=status.HTTP_201_CREATED)


# Single post detail (with comments)
#This endpoint lets anyone (no authentication required) view a specific post and its comments by providing the post ID.
class PostDetail(APIView):
    """
    GET: return single post with its comments (public)
    """

    def get(self, request, pk): #see post by ID
        post = next((p for p in in_memory.POSTS if p["id"] == pk), None)
        if not post:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        comments = [c for c in in_memory.COMMENTS if c["post"] == pk] #collects all comments
        return Response({**post, "comments": comments})


# Add comment to a post
#lets an authenticated user add a comment to an existing post.
class CommentCreate(APIView):
    """
    POST: add a comment to a specific post (auth required)
    """

    def post(self, request, pk):
        user = get_user_from_token(request)
        if not user:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        post = next((p for p in in_memory.POSTS if p["id"] == pk), None)
        if not post:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        text = (request.data.get("text") if request.data else "").strip()
        if not text:
            return Response({"text": "Text is required."}, status=status.HTTP_400_BAD_REQUEST)
        if len(text) > 500:
            return Response({"text": "Text must be <= 500 characters."}, status=status.HTTP_400_BAD_REQUEST)

        #creates dictionary for the comment with ID, post ID, user ID & timestamp
        comment = {
            "id": in_memory.get_next_comment_id(),
            "post": pk,
            "text": text,
            "author": user["id"],
            "created_at": in_memory._now(),
        }
        in_memory.COMMENTS.append(comment)
        return Response(comment, status=status.HTTP_201_CREATED)
