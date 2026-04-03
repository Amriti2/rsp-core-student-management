# RSP Core Student Management System

A modern, web-based student management platform built with Flask, Firebase, and Tailwind CSS. Features real-time chat, academic tracking, and principal oversight.

## 🚀 Features

- **Student Dashboard**: Track subjects, notes, and academic progress
- **Principal Control**: Manage students, send notifications, and oversee communications
- **Real-Time Chat**: Instant messaging between students and principals
- **Responsive Design**: Works on desktop and mobile devices
- **Firebase Integration**: Secure data storage and authentication

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Database**: Firebase Firestore
- **Deployment**: Desktop app via PyWebView

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Amriti2/rsp-core-student-management.git
   cd rsp-core-student-management
   ```

2. Set up virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install flask firebase-admin pywebview
   ```

4. Add your Firebase service account key as `rsp-system-firebase-adminsdk-*.json`

5. Run the app:
   ```bash
   python run_app.py
   ```

## 🔐 Configuration

- Place your Firebase service account JSON file in the project root
- Update Firebase config in `templates/*.html` if needed
- Ensure Firestore rules allow read/write for authenticated users

## 📱 Usage

- **Students**: Sign up, log in, update profile, chat with principal
- **Principals**: Use username `amran_principal` to access admin features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Amriti2** - *Initial work*

## 🙏 Acknowledgments

- Flask for the web framework
- Firebase for backend services
- Tailwind CSS for styling