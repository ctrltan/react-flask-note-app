
import { render, screen } from '@testing-library/react';
import axios from 'axios';
import HomePage from "./HomePage";

jest.mock('axios');

describe('HomePage', () => {
    it('should render home page without crashing', () => {
        render(<HomePage />);
        expect(screen.getByTestId('api')).toBeInTheDocument();
    });
});