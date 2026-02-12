# CropGuard AI - Multi-Page Application Guide

## 🎯 Application Flow

### Page 1: Authentication (`index.html`)
**Purpose**: User login and registration

**Features**:
- Tab-based interface (Login/Register)
- Form validation
- Error handling
- Auto-redirect if already logged in
- Redirect to dashboard on successful authentication

**Files**:
- `index.html` - Authentication page structure
- `auth.css` - Styling for auth page
- `auth.js` - Login/register logic

---

### Page 2: Dashboard (`dashboard.html`)
**Purpose**: Crop disease analysis

**Features**:
- Navbar with user info and logout
- Image upload with drag & drop support
- Image preview
- Crop type and location inputs
- Disease prediction
- Results display with recommendations
- Session protection (redirects to login if not authenticated)

**Files**:
- `dashboard.html` - Dashboard page structure
- `dashboard.css` - Styling for dashboard
- `dashboard.js` - Analysis logic

---

## 🚀 Quick Start Guide

### 1. Start Backend Server
```bash
cd backend
python app.py
```
Server runs on: `http://127.0.0.1:5000`

### 2. Open Application
Open in browser: `frontend/index.html`

### 3. Test Flow

**Step 1: Register**
1. Click "Register" tab
2. Enter name, email, password
3. Click "Register"
4. → Automatically redirected to dashboard

**Step 2: Upload & Analyze**
1. Click upload area or drag image
2. Enter crop type (e.g., "Tomato")
3. Enter location (e.g., "Farm A")
4. Click "Analyze Crop"
5. View results

**Step 3: Logout**
1. Click "Logout" button in navbar
2. → Redirected back to login page

---

## 📁 File Structure

```
frontend/
├── index.html          # Authentication page
├── dashboard.html      # Dashboard page
├── auth.css           # Auth page styles
├── dashboard.css      # Dashboard styles
├── auth.js            # Auth logic
├── dashboard.js       # Dashboard logic
├── app.js             # (old file - not used)
└── style.css          # (old file - not used)
```

---

## 🔐 Session Management

**How it works**:
- User credentials stored in `localStorage`
- `email` - User's email address
- `userName` - User's display name

**Auto-redirects**:
- Login page → Dashboard (if already logged in)
- Dashboard → Login page (if not logged in)

**Logout**:
- Clears localStorage
- Redirects to login page

---

## 🎨 Design Features

### Authentication Page
- Centered card design
- Gradient background
- Smooth animations
- Tab switching
- Responsive layout

### Dashboard Page
- Professional navbar
- Large upload area with hover effects
- Image preview
- Two-column form layout
- Animated results card
- Color-coded severity levels

---

## 🧪 Testing Scenarios

### Test 1: Registration Flow
1. Open `index.html`
2. Click "Register"
3. Fill: Name, Email, Password
4. Click "Register"
5. ✅ Should redirect to dashboard
6. ✅ Should show user name in navbar

### Test 2: Login Flow
1. Click "Logout" (if logged in)
2. Click "Login" tab
3. Enter email and password
4. Click "Login"
5. ✅ Should redirect to dashboard

### Test 3: Session Persistence
1. Login successfully
2. Close browser tab
3. Reopen `index.html`
4. ✅ Should auto-redirect to dashboard

### Test 4: Protected Dashboard
1. Logout
2. Try to open `dashboard.html` directly
3. ✅ Should redirect to login page

### Test 5: Image Upload
1. Login to dashboard
2. Click upload area
3. Select an image
4. ✅ Should show preview below

### Test 6: Disease Analysis
1. Upload image
2. Enter crop type and location
3. Click "Analyze Crop"
4. ✅ Button shows "Analyzing..."
5. ✅ Results appear in card format

---

## ⚠️ Important Notes

### Backend Requirements
- Flask server must be running on port 5000
- MongoDB connection (optional for basic UI testing)
- AI model file for actual predictions

### Browser Compatibility
- Modern browsers (Chrome, Firefox, Edge, Safari)
- JavaScript must be enabled
- LocalStorage must be enabled

### Known Limitations
1. **No AI Model**: Predictions will fail without model file
2. **No Database**: User data won't persist between sessions
3. **No Storage**: Uploaded images aren't saved
4. **Client-side Auth**: Not secure for production (demo only)

---

## 🔧 Troubleshooting

### "Network error" on login
- Check backend is running: `http://127.0.0.1:5000`
- Check browser console for CORS errors
- Verify API endpoint in `auth.js`

### Stuck on login page after successful login
- Check browser console for errors
- Verify `localStorage` is enabled
- Clear browser cache and try again

### Dashboard redirects to login immediately
- Check `localStorage` has `email` key
- Try logging in again
- Check browser console for errors

### Image preview not showing
- Check file format (jpg, png supported)
- Check file size (browser limits)
- Check browser console for errors

### "Analyzing..." never completes
- Check backend is running
- Check network tab in browser dev tools
- Verify backend has model file
- Check backend terminal for errors

---

## 🎯 Next Steps

### For Full Functionality
1. Add AI model file to `model/model.h5`
2. Set up MongoDB connection
3. Create storage directory
4. Test with real crop images

### For Production
1. Implement server-side authentication
2. Add JWT tokens
3. Use HTTPS
4. Add password hashing verification
5. Implement rate limiting
6. Add email verification
7. Add password reset
8. Deploy to cloud platform

---

## 📞 Support

If you encounter issues:
1. Check browser console (F12)
2. Check backend terminal logs
3. Verify all files are in correct locations
4. Ensure backend is running
5. Clear browser cache and localStorage
