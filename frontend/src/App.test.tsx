import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import App from './App'

describe('GapMap application shell', () => {
  it('shows the product purpose and primary diagnostic action', () => {
    render(<App />)

    expect(
      screen.getByRole('heading', {
        name: /find the prerequisite, not just the wrong answer/i,
      }),
    ).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /start diagnostic/i })).toBeInTheDocument()
  })
})
