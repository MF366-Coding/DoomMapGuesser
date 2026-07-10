using System;
using System.Globalization;

using Avalonia.Data.Converters;


namespace DoomMapGuessr.Helpers;


    /// <summary>
    /// A converter that multiplies two values.
    /// </summary>
    public class MultiplyConverter : IValueConverter
    {

        /// <summary>
        /// Converts a multiplication into the product (result).
        /// </summary>
        /// <param name="value">The first factor - <see cref="Double" /></param>
        /// <param name="targetType">Ignored.</param>
        /// <param name="parameter">The second factor - <see cref="Double" /> as <see cref="String" /></param>
        /// <param name="culture">Ignored.</param>
        /// <returns>The product or <paramref name="value" /></returns>
        public object? Convert(
            object? value,
            Type targetType,
            object? parameter,
            CultureInfo culture
        ) =>
            value is double d && parameter is string param && Double.TryParse(param, out double multiplier)
                ? d * multiplier
                : value;

        /// <summary>
        /// Converts a division into the quotient (result).
        /// </summary>
        /// <param name="value">The product of a multiplication - the dividend - <see cref="Double" /></param>
        /// <param name="targetType">Ignored.</param>
        /// <param name="parameter">The divisor - <see cref="Double" /> as <see cref="String" /> - different from <c>0</c></param>
        /// <param name="culture">Ignored.</param>
        /// <returns>The quotient or <paramref name="value" /></returns>
        public object? ConvertBack(
            object? value,
            Type targetType,
            object? parameter,
            CultureInfo culture
        ) =>
            value is double d && parameter is string param && Double.TryParse(param, out double multiplier) && multiplier != 0
                ? d / multiplier
                : value;

    }
