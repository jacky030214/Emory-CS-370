import React from 'react'
import { useNavigate } from 'react-router-dom'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function Dashboard_Page() {
  const navigate = useNavigate();

  const handleLogout = () => {
    navigate('/login');
  };

  // 학업 진행도 데이터 예시
  const progressData = {
    name: "Andrew",
    school: "Emory University",
    year: "Junior",
    credits: [
      { semester: "1-1", completed: 18, total: 21 },
      { semester: "1-2", completed: 19, total: 21 },
      { semester: "2-1", completed: 21, total: 21 },
      { semester: "2-2", completed: 18, total: 21 },
      { semester: "3-1", completed: 15, total: 21 },
      { semester: "3-2", completed: 0, total: 21 }
    ]
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm">
        <div className="w-full px-4">
            <div className="flex h-16"> {/* justify-between 제거 */}
                <div className="flex items-center">
                    <button 
                        onClick={() => navigate('/')}
                        className="text-2xl font-bold text-blue-600 hover:text-blue-700 transition-colors"
                    >
                        DegreeFlow 🚀
                    </button>
                </div>
            <div className="flex items-center ml-auto space-x-4"> {/* ml-auto 추가 */}
                <button 
                    onClick={() => navigate('/settings')}
                    className="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 rounded-md"
                >
                    Settings
                </button>
                <button 
                    onClick={() => navigate('/profile')}
                    className="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 rounded-md"
                >
                    Profile
                </button>
                <button 
                onClick={handleLogout}
                className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md"
                >
                    LOG OUT
                </button>
                    </div>
                </div>
            </div>
        </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Student info card */}
        <div className="bg-white shadow rounded-lg p-6 mb-6">
          <div className="grid grid-cols-3 gap-6">
            <div>
              <h2 className="text-sm font-medium text-gray-500">Name</h2>
              <p className="mt-1 text-lg font-semibold text-gray-900">{progressData.name}</p>
            </div>
            <div>
              <h2 className="text-sm font-medium text-gray-500">Shcool</h2>
              <p className="mt-1 text-lg font-semibold text-gray-900">{progressData.school}</p>
            </div>
            <div>
              <h2 className="text-sm font-medium text-gray-500">Year</h2>
              <p className="mt-1 text-lg font-semibold text-gray-900">{progressData.year}</p>
            </div>
          </div>
        </div>

        {/* 학업 진행도 그래프 */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Complete Credit per Semester</h2>
          <div className="w-full h-96">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={progressData.credits}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="semester" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="completed" name="이수 학점" fill="#3B82F6" />
                <Bar dataKey="total" name="총 학점" fill="#93C5FD" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </main>
    </div>
  )
}

export default Dashboard_Page