const API_BASE = import.meta.env.VITE_API_BASE || '';

export async function apiFetch(path, options = {}) {
  const { body, headers, ...rest } = options;
  const request = {
    credentials: 'include',
    headers: {
      ...(headers || {}),
    },
    ...rest,
  };

  if (body !== undefined) {
    request.body = typeof body === 'string' ? body : JSON.stringify(body);
    if (!request.headers['Content-Type']) {
      request.headers['Content-Type'] = 'application/json';
    }
  }

  return fetch(`${API_BASE}${path}`, request);
}

export async function readError(res) {
  try {
    const data = await res.json();
    if (data && typeof data.error === 'string') {
      return data.error;
    }
  } catch (err) {
    
  }
  return null;
}
