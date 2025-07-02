# 🍎 Apple Store - Premium E-commerce Experience

A stunning, modern e-commerce application inspired by Apple's design philosophy. Built with NiceGUI for rapid development and beautiful user interfaces.

## ✨ Features

### 🛍️ Customer Experience
- **Beautiful Product Catalog** - Apple-inspired design with smooth animations
- **Real-time Shopping Cart** - Instant updates and seamless cart management
- **Category Filtering** - Browse by iPhone, iPad, Mac, Watch, AirPods, and Accessories
- **Responsive Design** - Perfect experience on desktop, tablet, and mobile
- **Professional UI/UX** - Clean, minimalist design with premium feel

### 🔧 Admin Features
- **Product Management** - Add, edit, and delete products
- **Inventory Tracking** - Real-time stock management
- **Category Organization** - Organize products by Apple categories
- **Image Management** - Support for product images via URLs

### 🚀 Technical Excellence
- **Modern Architecture** - Clean separation of concerns with services layer
- **Real-time Updates** - Live cart updates and inventory changes
- **Database Integration** - SQLAlchemy with SQLite for data persistence
- **Type Safety** - Comprehensive type hints throughout
- **Error Handling** - Graceful error handling with user feedback
- **Production Ready** - Docker containerization and Fly.io deployment

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Installation

1. **Clone and Setup**
```bash
git clone <repository-url>
cd apple-store
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

4. **Run the Application**
```bash
python main.py
```

5. **Access the Store**
- **Main Store**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **Health Check**: http://localhost:8000/health

## 🏗️ Project Structure

```
apple-store/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── dockerfile             # Container configuration
├── fly.toml               # Deployment configuration
├── .env                   # Environment variables
├── README.md              # This file
├── app/
│   ├── main.py            # Main application logic
│   ├── config.py          # Configuration management
│   └── components/        # UI components
│       ├── product_card.py
│       ├── cart_sidebar.py
│       └── admin_panel.py
├── models/
│   └── schemas.py         # Data models and database schemas
├── services/
│   ├── product_service.py # Product business logic
│   └── cart_service.py    # Cart management logic
├── core/
│   └── database.py        # Database configuration
└── static/
    ├── css/               # Custom styles
    └── images/            # Product images
```

## 🎨 Design Philosophy

### Apple-Inspired Aesthetics
- **Clean Minimalism** - Lots of white space and clean lines
- **Premium Typography** - San Francisco-inspired system fonts
- **Subtle Animations** - Smooth transitions and hover effects
- **Color Palette** - Apple's signature blues, grays, and whites
- **Glass Effects** - Modern backdrop blur and transparency

### User Experience
- **30-Second Value** - Immediate understanding of the store's purpose
- **Intuitive Navigation** - Clear category organization
- **Responsive Design** - Seamless experience across all devices
- **Performance** - Fast loading and smooth interactions

## 🛠️ Configuration

### Environment Variables

```bash
# Application Settings
APP_NAME=Apple Store
DEBUG=true

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=sqlite:///./apple_store.db

# Security
SECRET_KEY=your-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Store Settings
STORE_NAME=Apple Store
CURRENCY=USD
TAX_RATE=0.08
```

### Admin Access
- **Username**: admin (configurable via ADMIN_USERNAME)
- **Password**: admin123 (configurable via ADMIN_PASSWORD)

## 🐳 Docker Deployment

### Build and Run
```bash
# Build the image
docker build -t apple-store .

# Run the container
docker run -p 8000:8000 apple-store
```

### Docker Compose (Optional)
```yaml
version: '3.8'
services:
  apple-store:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./data/apple_store.db
    volumes:
      - ./data:/app/data
```

## ☁️ Fly.io Deployment

### Deploy to Fly.io
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login to Fly.io
fly auth login

# Deploy the application
fly deploy
```

### Configuration
The `fly.toml` file is pre-configured with:
- **Auto-scaling** - Scales to zero when not in use
- **Health checks** - Automatic health monitoring
- **HTTPS** - Automatic SSL certificates
- **Regional deployment** - Optimized for performance

## 🧪 Testing

### Manual Testing Checklist
- [ ] Product catalog loads correctly
- [ ] Category filtering works
- [ ] Add to cart functionality
- [ ] Cart updates in real-time
- [ ] Admin panel accessible
- [ ] Product creation/deletion
- [ ] Responsive design on mobile
- [ ] Error handling graceful

### Load Testing
```bash
# Install dependencies
pip install locust

# Run load tests (if implemented)
locust -f tests/load_test.py --host=http://localhost:8000
```

## 🔧 Development

### Adding New Products
1. Access admin panel at `/admin`
2. Fill in product details
3. Add high-quality product images
4. Set appropriate category and stock levels

### Customizing Design
- Modify CSS variables in `app/main.py` head HTML
- Update component styles in `app/components/`
- Add custom CSS in `static/css/styles.css`

### Extending Functionality
- Add payment processing in `services/`
- Implement user authentication
- Add product reviews and ratings
- Integrate with external APIs

## 📊 Performance

### Optimization Features
- **Lazy Loading** - Images and components load on demand
- **Efficient Queries** - Optimized database operations
- **Caching** - Strategic caching for better performance
- **Compression** - Optimized assets and responses

### Monitoring
- Health check endpoint at `/health`
- Built-in error logging
- Performance metrics collection ready

## 🔒 Security

### Security Features
- **Input Validation** - Pydantic models for all data
- **SQL Injection Prevention** - Parameterized queries
- **XSS Protection** - Proper output encoding
- **Secure Headers** - Security-focused HTTP headers
- **Admin Authentication** - Protected admin routes

### Best Practices
- Environment-based configuration
- Secrets management via environment variables
- Secure session handling
- Regular dependency updates

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Standards
- Follow PEP 8 style guidelines
- Add type hints to all functions
- Include docstrings for public methods
- Write tests for new features

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Common Issues

**Database Connection Errors**
```bash
# Reset database
rm apple_store.db
python main.py
```

**Dependency Conflicts**
```bash
# Clean install
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

**Port Already in Use**
```bash
# Change port in .env
PORT=8001
```

### Getting Help
- Check the logs for detailed error messages
- Verify all dependencies are installed correctly
- Ensure Python 3.10+ is being used
- Check environment variable configuration

## 🚀 What's Next?

### Planned Features
- [ ] User authentication and profiles
- [ ] Payment processing integration
- [ ] Product reviews and ratings
- [ ] Wishlist functionality
- [ ] Order history and tracking
- [ ] Email notifications
- [ ] Advanced search and filtering
- [ ] Product recommendations
- [ ] Multi-language support
- [ ] Analytics dashboard

---

**Built with ❤️ using NiceGUI and modern Python practices**

*Experience the future of e-commerce with Apple-inspired design and cutting-edge technology.*