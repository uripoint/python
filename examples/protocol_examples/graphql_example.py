"""
Example demonstrating GraphQL protocol support in UriPoint
"""
from uripoint import UriPointCLI

def setup_graphql_endpoints():
    """Setup GraphQL API endpoints"""
    cli = UriPointCLI()

    # Main GraphQL API
    cli.create_endpoint(
        uri='http://localhost:4000/graphql',
        data={
            'schema': '''
                type User {
                    id: ID!
                    name: String!
                    email: String!
                    posts: [Post!]!
                    profile: Profile
                }

                type Post {
                    id: ID!
                    title: String!
                    content: String!
                    author: User!
                    comments: [Comment!]!
                    tags: [String!]!
                    createdAt: String!
                }

                type Comment {
                    id: ID!
                    content: String!
                    author: User!
                    post: Post!
                    createdAt: String!
                }

                type Profile {
                    bio: String
                    location: String
                    website: String
                    socialLinks: [String!]
                }

                type Query {
                    user(id: ID!): User
                    users(limit: Int = 10): [User!]!
                    post(id: ID!): Post
                    posts(
                        limit: Int = 10
                        offset: Int = 0
                        tag: String
                    ): [Post!]!
                    comments(postId: ID!): [Comment!]!
                }

                type Mutation {
                    createUser(
                        name: String!
                        email: String!
                    ): User!
                    
                    updateProfile(
                        userId: ID!
                        bio: String
                        location: String
                        website: String
                        socialLinks: [String!]
                    ): Profile!
                    
                    createPost(
                        title: String!
                        content: String!
                        authorId: ID!
                        tags: [String!]!
                    ): Post!
                    
                    addComment(
                        content: String!
                        postId: ID!
                        authorId: ID!
                    ): Comment!
                }

                type Subscription {
                    newPost: Post!
                    newComment(postId: ID!): Comment!
                    userActivity(userId: ID!): User!
                }
            ''',
            'resolvers': {
                'Query': {
                    'user': {'type': 'database', 'table': 'users'},
                    'users': {'type': 'database', 'table': 'users'},
                    'post': {'type': 'database', 'table': 'posts'},
                    'posts': {'type': 'database', 'table': 'posts'},
                    'comments': {'type': 'database', 'table': 'comments'}
                },
                'Mutation': {
                    'createUser': {'type': 'function', 'handler': 'create_user'},
                    'updateProfile': {'type': 'function', 'handler': 'update_profile'},
                    'createPost': {'type': 'function', 'handler': 'create_post'},
                    'addComment': {'type': 'function', 'handler': 'add_comment'}
                },
                'Subscription': {
                    'newPost': {'type': 'pubsub', 'topic': 'posts'},
                    'newComment': {'type': 'pubsub', 'topic': 'comments'},
                    'userActivity': {'type': 'pubsub', 'topic': 'users'}
                }
            },
            'middleware': [
                'authentication',
                'logging',
                'caching',
                'validation'
            ],
            'options': {
                'introspection': True,
                'playground': True
            }
        }
    )

    # GraphQL Subscriptions
    cli.create_endpoint(
        uri='ws://localhost:4000/graphql/subscriptions',
        data={
            'type': 'subscription',
            'protocol': 'graphql-ws',
            'topics': ['posts', 'comments', 'users']
        }
    )

    print("\nGraphQL endpoints created:")
    print("1. Main API:")
    print("   - URI: http://localhost:4000/graphql")
    print("   - Playground: http://localhost:4000/graphql/playground")
    print("   - Types: User, Post, Comment, Profile")
    print("   - Operations: Query, Mutation, Subscription")
    
    print("\n2. Subscriptions:")
    print("   - URI: ws://localhost:4000/graphql/subscriptions")
    print("   - Topics: posts, comments, users")

def test_graphql_queries():
    """Test GraphQL queries"""
    cli = UriPointCLI()

    # Query users
    users_query = '''
    query {
        users(limit: 5) {
            id
            name
            email
            posts {
                title
            }
        }
    }
    '''
    cli.publish('http://localhost:4000/graphql', {'query': users_query})

    # Create user mutation
    create_user_mutation = '''
    mutation {
        createUser(
            name: "John Doe"
            email: "john@example.com"
        ) {
            id
            name
            email
        }
    }
    '''
    cli.publish('http://localhost:4000/graphql', {'query': create_user_mutation})

    # Subscribe to new posts
    subscription = '''
    subscription {
        newPost {
            id
            title
            author {
                name
            }
        }
    }
    '''
    cli.subscribe('ws://localhost:4000/graphql/subscriptions', 
                 {'query': subscription},
                 lambda data: print(f"New post: {data}"))

if __name__ == '__main__':
    print("Setting up GraphQL endpoints...")
    setup_graphql_endpoints()
    
    print("\nTesting GraphQL operations...")
    test_graphql_queries()
