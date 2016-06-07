# Documentation for subtree here
http://blogs.atlassian.com/2013/05/alternatives-to-git-submodule-git-subtree/

# Add a project as a subtree
git remote add -f Microservices_OrdersAPI git@github.com:hassenius/Microservices_OrdersAPI.git

# Clone the project
git subtree add --prefix Microservices_OrdersAPI Microservices_OrdersAPI

# Push changes to subtree project
git subtree push --prefix=Microservices_OrdersAPI Microservices_OrdersAPI master

# Push changes to root project
git push origin master


