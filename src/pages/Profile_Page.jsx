// src/pages/Profile_Page.jsx
import React, { useState } from 'react'
import userInfo from '../DATA/userInfo.json'  // 경로 수정

function Profile_Page() {
  console.log('userInfo:', userInfo); // 데이터가 제대로 불러와지는지 확인
  const [userEmail, setUserEmail] = useState(userInfo.email);

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">Profile</h1>
            </div>
          </div>
        </div>
      </nav>
      
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Profile Information</h2>
            <div className="space-y-4">
              <div className="border-b pb-4">
                <p className="text-sm text-gray-500">Email</p>
                <p className="text-lg font-medium text-gray-900">{userEmail}</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default Profile_Page