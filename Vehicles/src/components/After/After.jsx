import React from 'react'

function After({imageurl}) {
  return (

<div className="max-w-sm mt-4 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
  <a href={imageurl} target="_blank" rel="noopener noreferrer">
    <img className="rounded-t-lg" src={imageurl} alt="" />
  </a>
</div>
  )
}

export default After