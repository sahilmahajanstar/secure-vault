import './style/home.css'

// import { Link } from 'react-router-dom';

export const Home = () => {
    return (
        <div className="home-container">
            {/* <nav className="home-nav">
        <div className="logo">SecureVault</div>
        <div className="nav-links">
          <Link to="/users/login">Login</Link>
          <Link to="/users/register" className="register-btn">Get Started</Link>
        </div>
      </nav> */}

            <main className="hero-section">
                <div className="hero-content">
                    <h1>Your Personal Secure Vault</h1>
                    <p className="hero-subtitle">
                        Store and Share your files with your friends and family
                    </p>
                </div>

                <div className="features-grid">
                    <div className="feature-card">
                        <span className="feature-icon">🔒</span>
                        <h3>End-to-End Encryption</h3>
                        <p>
                            Your data is encrypted before it leaves your device
                        </p>
                    </div>
                    <div className="feature-card">
                        <span className="feature-icon">📱</span>
                        <h3>Share Files</h3>
                        <p>Share your files with your friends and family</p>
                    </div>
                    <div className="feature-card">
                        <span className="feature-icon">🛡️</span>
                        <h3>Zero-Knowledge</h3>
                        <p>We can't read your data - only you have access</p>
                    </div>
                </div>
            </main>
        </div>
    )
}
