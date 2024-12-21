import './style/userInfo.css'

import Logout from '../../common/components/Logout'
import React from 'react'
import { useAppSelector } from '../../config/redux/hooks'

const UserInfo: React.FC = () => {
    const user = useAppSelector(state => state.user.user)
    return (
        <div className="user-info-container">
            <h2>User Profile</h2>
            {user ? (
                <div className="user-details">
                    <p>
                        <strong>Email:</strong> {user.email}
                    </p>
                    <p>
                        <strong>name:</strong> {user.firstName} {user.lastName}
                    </p>
                    <p>
                        <strong>verification status:</strong>{' '}
                        {user.emailVerified ? 'true' : 'false'}
                    </p>
                    <p>
                        <strong>roleone:</strong> {user.role}
                    </p>
                    {/* Add more user details as needed */}
                </div>
            ) : (
                <p>No user information available.</p>
            )}
            <Logout />
        </div>
    )
}

export default UserInfo
