import './styles/stickyHeader.css'

import { If } from './If'
import { Link } from 'react-router-dom'
import React from 'react'
import { useAppSelector } from '../../config/redux/hooks'

const StickyHeader: React.FC = () => {
    const isAuthenticated = useAppSelector(state => state.user.isAuthenticated)
    return (
        <header className="sticky-header">
            <nav className="nav-container">
                <div className="logo">SecureVault</div>
                <ul className="nav-links">
                    <li>
                        <Link to="/">Home</Link>
                    </li>
                    <If condition={!isAuthenticated}>
                        <li>
                            <Link to="/users/login">Login</Link>
                        </li>
                        <li>
                            <Link to="/users/register">Register</Link>
                        </li>
                    </If>
                    <If condition={isAuthenticated}>
                        <li className="dropdown">
                            <Link to="/files/list">
                                Files <i className="fa fa-caret-down"></i>
                            </Link>
                            <ul className="dropdown-menu">
                                <li>
                                    <Link to="/files/upload">Upload</Link>
                                </li>
                                <li>
                                    <Link to="/files/share-with-you">
                                        Share with you
                                    </Link>
                                </li>
                            </ul>
                        </li>
                        <li>
                            <Link to="/user/info">Profile</Link>
                        </li>
                    </If>
                </ul>
            </nav>
        </header>
    )
}
export default StickyHeader
